import json
import os
import boto3
from datetime import datetime

ecs_client = boto3.client('ecs')

# Environment variables
ECS_CLUSTER_NAME = os.environ['ECS_CLUSTER_NAME']
ECS_SERVICE_NAME = os.environ['ECS_SERVICE_NAME']
MIN_TASKS = int(os.environ.get('MIN_TASKS', 1))
MAX_TASKS = int(os.environ.get('MAX_TASKS', 10))

def handler(event, context):
    """
    Lambda handler triggered by SQS messages from S3 events.
    Scales ECS service based on the number of files uploaded.
    """
    
    print(f"Event received: {json.dumps(event)}")
    
    # Get number of messages in the batch
    num_messages = len(event.get('Records', []))
    
    if num_messages == 0:
        print("No messages to process")
        return {
            'statusCode': 200,
            'body': json.dumps('No messages to process')
        }
    
    # Parse S3 events from SQS messages
    s3_events = []
    for record in event['Records']:
        try:
            # SQS body contains the S3 event
            body = json.loads(record['body'])
            
            # S3 event can contain multiple records
            if 'Records' in body:
                for s3_record in body['Records']:
                    if 's3' in s3_record:
                        bucket = s3_record['s3']['bucket']['name']
                        key = s3_record['s3']['object']['key']
                        s3_events.append({
                            'bucket': bucket,
                            'key': key,
                            'eventTime': s3_record['eventTime']
                        })
                        print(f"S3 object uploaded: s3://{bucket}/{key}")
        except Exception as e:
            print(f"Error parsing message: {str(e)}")
            continue
    
    print(f"Total S3 events processed: {len(s3_events)}")
    
    # Get current ECS service status
    try:
        response = ecs_client.describe_services(
            cluster=ECS_CLUSTER_NAME,
            services=[ECS_SERVICE_NAME]
        )
        
        if not response['services']:
            print(f"Service {ECS_SERVICE_NAME} not found in cluster {ECS_CLUSTER_NAME}")
            return {
                'statusCode': 404,
                'body': json.dumps('ECS service not found')
            }
        
        service = response['services'][0]
        current_desired_count = service['desiredCount']
        running_count = service['runningCount']
        
        print(f"Current desired count: {current_desired_count}, Running count: {running_count}")
        
        # Calculate new desired count based on workload
        # Strategy: Scale up by 1 task for every 5 new files (you can adjust this logic)
        scale_factor = max(1, len(s3_events) // 5)
        new_desired_count = min(current_desired_count + scale_factor, MAX_TASKS)
        
        # Ensure we don't go below minimum
        new_desired_count = max(new_desired_count, MIN_TASKS)
        
        print(f"Calculated new desired count: {new_desired_count}")
        
        # Update service if needed
        if new_desired_count != current_desired_count:
            print(f"Scaling ECS service from {current_desired_count} to {new_desired_count} tasks")
            
            update_response = ecs_client.update_service(
                cluster=ECS_CLUSTER_NAME,
                service=ECS_SERVICE_NAME,
                desiredCount=new_desired_count
            )
            
            print(f"Service updated successfully")
            
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'ECS service scaled successfully',
                    'previous_count': current_desired_count,
                    'new_count': new_desired_count,
                    's3_events_processed': len(s3_events)
                })
            }
        else:
            print(f"No scaling needed. Current count: {current_desired_count}")
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'No scaling needed',
                    'current_count': current_desired_count,
                    's3_events_processed': len(s3_events)
                })
            }
            
    except Exception as e:
        print(f"Error scaling ECS service: {str(e)}")
        raise e