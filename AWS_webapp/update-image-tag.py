# Author: Jiawei

import boto3
import json
from decimal import Decimal

# Initialise the DynamoDB and the item existing identifier
database = boto3.resource('dynamodb')

def lambda_handler(event, context):
    found_image = True
    try:
        API = json.loads(event['body'])
        image_id = API['key']
        
        tag = API['tags']
        
        order = API['type']
        print(image_id)
    
        table = database.Table('image-metadata')
        
        response = table.get_item(
            Key = {
                'key': image_id
            }
        )
    
        if 'Item' in response:
            print("Item exists in DynamoDB")
            found_image = True
        else:
            print("Item does not exist in DynamoDB")
            found_image = False
            
        print(found_image)    
        if found_image and order == 1:
    
            for addtag in tag:
                # Check if 'count' is in the dictionary, if not default to 1
                count = addtag['count'] if 'count' in addtag else 1
                response = table.update_item(
                    Key={
                        'key': image_id
                    },
                    UpdateExpression=f'SET tags.#tag = :val',
                    ExpressionAttributeNames={
                        '#tag': addtag['tag'],
                    },
                    ExpressionAttributeValues={
                        ':val': Decimal(count)
                    },
                    ReturnValues='UPDATED_NEW'
                )
    
            
            print(response)
            
            response = {}
            response['statusCode'] = 200
            response['body'] = 'Tag removed successfully'
            response['headers'] = {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
            }
            return response
        elif found_image and order == 0:
            response = table.get_item(
                Key={
                    'key': image_id
                }
            )
            item = response['Item']
            
            # Then, for each tag in the list, decrement the count or remove the tag
            for remtag in tag:
                tag = remtag['tag']
                count = remtag['count'] if 'count' in remtag else 1
            
                if tag in item['tags']:
                    if item['tags'][tag] > count:
                        item['tags'][tag] -= Decimal(count)
                    else:
                        del item['tags'][tag]
            
            # Finally, write the item back to DynamoDB
            response = table.put_item(Item=item)
            
            response = {}
            response['statusCode'] = 200
            response['body'] = 'Tag removed successfully'
            response['headers'] = {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
            }
            return response
            
        else:
            response = {'error': 'Image not found in database'}
            response['headers'] = {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
            }
            return response
    except e:
        response = {'body': e, 'statusCode': 200 }
        response['headers'] = {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
            }
        return response
            
