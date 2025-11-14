import boto3
import argparse
from packaging.version import Version

lambda_client = boto3.client('lambda')

def parse_arguments():
    parser = argparse.ArgumentParser(description='Update AWS Lambda function runtime.')
    parser.add_argument('--python_version', '-a', required=True, help=" Python version")
    return parser.parse_args()


def list_lambda_functions():
    response = lambda_client.list_functions()
    return response.get("Functions", [])

def compare_runtime(runtime, runtime_to_compare_with):
    return Version(runtime.split("python")[-1]) < Version(runtime_to_compare_with.split("python")[-1])

def update_function_runtime(function_name, old_runtime, new_runtime):
    print(f"Updating function: {function_name} from {old_runtime} to {new_runtime}")
    try:
        lambda_client.update_function_configuration(
            FunctionName=function_name,
            Runtime=new_runtime
        )
    except Exception as e:
        print(f"Error updating function {function_name}: {e}")

def function_runtime(lambda_json_list):
    temp_list = []
    for function in lambda_json_list:
        name = function.get("FunctionName", "")
        runtime = function.get("Runtime", None)
        if runtime:
            temp_list.append((name, runtime))
            print(f"Function Name: {name}, Runtime: {runtime}")
    return temp_list
        

def perform_update(new_runtime):
    data = function_runtime(list_lambda_functions() or [])
    temp = []
    for function_name, current_runtime in data:
        if compare_runtime(current_runtime, new_runtime):
            temp.append(function_name)
            update_function_runtime(function_name, current_runtime, new_runtime)
    if not temp:
        print("No functions required an update.")


if __name__ == "__main__":
    args = parse_arguments()
    new_python_version = args.python_version
    perform_update(new_python_version)