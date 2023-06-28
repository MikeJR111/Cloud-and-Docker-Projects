##  Author: Jiawei


import json
import boto3
from boto3.dynamodb.conditions import Key
from decimal import Decimal

database = boto3.resource('dynamodb')
table = database.Table('image-metadata')


def lambda_handler(event, context):
    # Extract the body from the event and parse it as JSON
    body = json.loads(event['body'])

    # Extract the tags from the body
    user_tags = body['tags']
    
    num_tags = len(user_tags)
    
    #print(num_tags)
    
    # get all items from db
    response = table.scan()
    data = response['Items']  
    
    url_list = []
    
    for index, element in enumerate(data):
        match = True
        
        url = element['key']
        item = element['tags']
        keys_list = list(item.keys())
        #print(keys_list)
        print(item)
        if len(keys_list) >  num_tags:
            for requirement in user_tags:
                tag = requirement['tag']
                required_count = requirement['count']
                
                if tag not in keys_list:
                    match = False
                elif tag in keys_list:
                    if int(item[tag]) < required_count:
                        match = False
            if match:
                url_list.append('https://kzhe0012-fit5225-a2-uploaded-images.s3.amazonaws.com/'+ url)
            
    result = {
        "links": url_list,
        'tags': keys_list
    }        
    
    print(result)
    
    # Return the result
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
        },
        'body': json.dumps(result),
        'isBase64Encoded': False
    }