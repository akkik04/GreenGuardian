import json
import boto3
import datetime

# function to read the modified JSON file created from the 'modify-batch-transform-job-output-func' from S3 and return the bounding box coordinates.
def get_bounding_box_coordinates(s3_bucket, s3_file_key):
    
    # initialize an S3 client.
    s3_client = boto3.client('s3')
    
    try:
        # fetch the JSON file from S3
        response = s3_client.get_object(Bucket=s3_bucket, Key=s3_file_key)
        
        # read the contents of the file
        file_content = response['Body'].read()
        
        # parse the JSON data
        json_data = json.loads(file_content)
        
        # extract the bounding box coordinates and the confidence from the JSON data.
        result = {}
        for key, val in json_data.items():
            if val and isinstance(val, list):
                coordinates = [item[-5:] for item in val if len(item) >= 5]
                jpeg_name = key.split('/')[-1].split('.out')[0]
                print(jpeg_name)
                result[jpeg_name] = coordinates
        print(json.dumps(result, indent=2))
        return result
    except Exception as e:
        print(f"Error reading JSON file from S3: {str(e)}")

def lambda_handler(event, context):
    
    # formatted_date = datetime.today().strftime('%Y-%m-%d')
    
    # TO-DO: Agnostic approach for the datetime of json file, as job only runs once a day.
    get_bounding_box_coordinates('green-guardian-batch-transformation', 'modified-outputs/2023-10-29/2023-10-29.json')