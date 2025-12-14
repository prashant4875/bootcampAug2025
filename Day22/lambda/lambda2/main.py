import pandas
import json
import boto3
from openpyxl import Workbook, load_workbook

def lambda_handler(event, context):
    """
    Simple AWS Lambda handler
    """
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Hello from Lambda'})
    }
