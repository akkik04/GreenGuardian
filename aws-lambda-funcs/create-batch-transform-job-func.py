import json
import boto3
from datetime import datetime

client = boto3.client('sagemaker')

def lambda_handler(event, context):
    
    # get the date for the job.
    current_datetime = datetime.today()
    formatted_date = current_datetime.strftime('%Y-%m-%d')
    formatted_time = current_datetime.strftime('%H-%M-%S')
    
    # create the batch transformation job.
    response = client.create_transform_job(
        TransformJobName = f'{formatted_date}-{formatted_time}-object-detection-unique',
        ModelName = 'green-guardian-detects-plastic',
        
        # maximum size of the payload for each individual image in the batch.
        MaxPayloadInMB = 100, 
        
        # set the transformation job's input.
        TransformInput = {
            'DataSource': {
                'S3DataSource': {
                    'S3DataType': 'S3Prefix',
                    # input path for the job's artifacts.
                    'S3Uri': f's3://green-guardian-batch-transformation/input-images/{current_datetime[0:4]}/{current_datetime[5:7]}/{current_datetime[8:10]}/'
                }
            },
            'ContentType' : 'image/jpeg',
            'CompressionType': 'None',
            'SplitType': 'None'
        },
        
        # set the transformation job's output.
        TransformOutput = {

            # output path for the job's artifacts.
            'S3OutputPath': f's3://green-guardian-batch-transformation/batch-output/{current_datetime[0:4]}/{current_datetime[5:7]}/{current_datetime[8:10]}/',
            'AssembleWith': 'None'
        },
        
        # provision the required resources.
        TransformResources = {
            'InstanceType': 'ml.m4.xlarge',
            'InstanceCount': 1
        },
        
        # include all the image data.
        DataProcessing = {
            'InputFilter': '$',
            'OutputFilter': '$',
            'JoinSource': 'None'
        }
    )
    
    # return the response from the batch transformation job.
    return {
        'body': response
    }