import json
import boto3
from datetime import datetime

# set-up the sagemaker client.
client = boto3.client('sagemaker') 

# get the date for the job.
current_datetime = datetime.today()
formatted_date = current_datetime.strftime('%Y-%m-%d')
    
def lambda_handler(event, context):
    try:
        # find and return the status of the batch transformation job.
        response = client.describe_transform_job(TransformJobName = f'{formatted_date}-green-guardian-object-detection')
        return response['TransformJobStatus']
    
    # catch any errors.
    except Exception as e:
        print(e)
        message = 'Error getting Batch  Transformation Job status'
        raise Exception(message)