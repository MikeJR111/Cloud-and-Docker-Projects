## Author: Jiawei

import boto3
import json

# Initialize the DynamoDB client
dynamodb = boto3.resource('dynamodb')

# Initialize the S3 client
s3 = boto3.client('s3')

# Assuming the table's name is 'your_table'
table = dynamodb.Table('image-metadata')

# The S3 bucket name
bucket_name = 'kzhe0012-fit5225-a2-uploaded-images'

def lambda_handler(event, context):
    # Parse the POST data from the event object
    post_data = json.loads(event['body'])

    # Extract the key from the POST data
    key = post_data['key']

    # First, delete the item from DynamoDB
    response = table.delete_item(
        Key={
            'key': key
        }
    )

    # Check if the item was successfully deleted
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print('Item deleted successfully from DynamoDB')

    # Then, delete the image from S3
    response = s3.delete_object(
        Bucket=bucket_name,
        Key=key
    )

    # Check if the image was successfully deleted
    if response['ResponseMetadata']['HTTPStatusCode'] == 204:
        print('Image deleted successfully from S3')

    return {
        'statusCode': 200,
        'headers': {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
        },
        'body': json.dumps('Image and database entry deleted successfully')
    }