import json
import boto3
import os
from datetime import datetime

# create a custom dictionary class for working with the .json data.
class MyDictionary(dict):
    def add(self, key, value):
        self[key] = value

# process the raw .json data from the batch transformation job.
def process_s3_data(BUCKET, FOLDER):

    # create a dictionary object to store the .json data.
    dict = MyDictionary()

    # init the s3 client.
    s3 = boto3.client('s3')
    
    # paginate through the s3 bucket.
    paginator = s3.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket = BUCKET, Prefix = FOLDER)
    
    # iterate through the pages and objects.
    for page in pages:
        for obj in page['Contents']:

            # get the .json file from s3.
            file_key = obj['Key']
            response = s3.get_object(Bucket = BUCKET, Key = file_key)

            # parse the .json file.
            found_these_detections = json.loads(response['Body'].read())['prediction']

            # iterate through the detections and add them to the dictionary.
            temp_arr = []
            for detections in found_these_detections:
                klass, score, x0, y0, x1, y1 = detections

                # filter out the low confidence detections.
                if score < 0.27:
                    continue

                # create the array to store the data.
                arr = [klass, score, x0, y0, x1, y1]
                temp_arr.append(arr)
            dict.add(file_key, temp_arr)
    
    # return the dictionary.
    return dict

# upload the processed .json data to s3.
def upload_to_s3(BUCKET, file_name, desired_name_s3):
    s3_resource = boto3.resource('s3')
    s3_resource.Bucket(BUCKET).upload_file(file_name, desired_name_s3)

    # delete the file from the aws lambda's tmp directory.
    os.remove(file_name)

def lambda_handler(event, context):

    # datetime stuff.
    current_datetime = datetime.today()
    formatted_date = current_datetime.strftime('%Y-%m-%d')
    
    # specify the bucket and folder to process.
    BUCKET = 'green-guardian-batch-transformation'
    FOLDER = f'batch-output/{formatted_date}'

    # create the modified results.
    results = json.dumps(process_s3_data(BUCKET, FOLDER), indent=4)
    
    # open aws lambda's tmp directory and write the results to a .json file.
    with open(f'/tmp/{formatted_date}.json', 'w') as out:
        out.write(results)
    
    # upload the modified results to s3.
    upload_filename = f"modified-outputs/{formatted_date}/{formatted_date}.json"
    upload_to_s3(BUCKET, f'/tmp/{formatted_date}.json', upload_filename)
    
    return {
        'body': results
    }