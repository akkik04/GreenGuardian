import json
import boto3
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.patches as patches
from io import BytesIO
import datetime

# helper function to draw the bounding boxes.
def draw_bounding_box(image, data_list):

    # set the S3 bucket name and file key.
    bucket_name = 'green-guardian-batch-transformation'

    # TO-DO: Agnostic approach for the datetime of json file, as job only runs once a day.
    file_key = f'input-images/2023-10-29/{image}'
    
    # initialize an S3 client.
    s3 = boto3.client('s3')
    try:
        # retrieve the JPG file from the S3 bucket
        response = s3.get_object(Bucket=bucket_name, Key=file_key)
        
        # read the contents of the file.
        image_content = response['Body'].read()
        img = plt.imread(BytesIO(image_content), format='jpg')

        # set-up the plot and get the original image's size for scaling the bounding box coordinates.
        fig, ax = plt.subplots()
        ax.imshow(img)
        img_height, img_width, _ = img.shape
        
        # store the current image's bounding box requirements.
        confidence = data_list[0]
        curr_xmin = data_list[1]
        curr_xmax = data_list[3]
        curr_ymin = data_list[2]
        curr_ymax = data_list[4]
        
        # modify the current image's bounding box requirements by multiplying by the factor for each axe's min&max.
        new_xmin = curr_xmin * img_width
        new_xmax = curr_xmax * img_width
        new_ymin = curr_ymin * img_height
        new_ymax = curr_ymax * img_height
        
        # retrieve the bounding boxes height and width.
        width = new_xmax - new_xmin
        height = new_ymax - new_ymin

        # add the bounding box to the plot.
        rect = patches.Rectangle((new_xmin,new_ymin), width, height, linewidth = 2, edgecolor = 'r', facecolor = 'none')
        ax.add_patch(rect)
        text = f'Confidence: {confidence:.2f}'
        bbox_props = dict(boxstyle='square,pad=0.3', fc='red', ec='white', lw=2)
        t = ax.text(rect.get_x(), rect.get_y(), text, ha='left', va='top', fontsize=12, color='white', bbox=bbox_props)
        
        # save the modified image as a PNG file in memory
        jpg_buffer = BytesIO()
        fig.savefig(jpg_buffer, format='jpg')
        jpg_data = jpg_buffer.getvalue()

        # upload the modified image to a different path or folder in the S3 bucket
        # change the Key argument to the desired path or folder name
        s3.put_object(Bucket=bucket_name, Key=f'inferenced-images/2023-10-29/{image}', Body=jpg_data)
        
    except Exception as e:
        print("Error:", e)

# helper function to retrieve the bounding box coordinates from the JSON file.
def get_bounding_box_coordinates(s3_bucket, s3_file_key):
    
    # initialize an S3 client.
    s3_client = boto3.client('s3')
    
    try:
        # fetch the JSON file from S3.
        response = s3_client.get_object(Bucket=s3_bucket, Key=s3_file_key)
        
        # read the contents of the file.
        file_content = response['Body'].read()
        
        # parse the JSON data.
        json_data = json.loads(file_content)
        
        result = {}
        for key, val in json_data.items():
            if val and isinstance(val, list):
                coordinates = [item[-5:] for item in val if len(item) >= 5]
                jpeg_name = key.split('/')[-1].split('.out')[0]
                result[jpeg_name] = coordinates
        return result
    
    except Exception as e:
        print(f"Error reading JSON file from S3: {str(e)}")

def lambda_handler(event, context):
    
    # formatted_date = datetime.today().strftime('%Y-%m-%d')
    
    # TO-DO: Agnostic approach for the datetime of json file, as job only runs once a day.
    json_data = get_bounding_box_coordinates('green-guardian-batch-transformation', 'modified-outputs/2023-10-29/2023-10-29.json')

    for image, data_lists in json_data.items():
        for data_list in data_lists:
            draw_bounding_box(image, data_list)

