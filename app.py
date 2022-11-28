import os

import boto3
import json

dynamodb = boto3.resource('dynamodb')
POSTS_TABLE = os.environ['POSTS_TABLE']
header = { "Content-Type": "application/json" }


def create_post(event, context):
    body = json.loads(event['body'])
    post_id = body['postId']
    title = body['title']

    table = dynamodb.Table(POSTS_TABLE)

    if not post_id or not title:
        return {"statusCode": 400, "body": json.dumps({'error': 'Please provide both "postId" and "title"'})}
    
    table.put_item(Item={ 'postId': post_id, 'title': title })

    return {"statusCode": 200, "headers": header, "body": json.dumps({'postId': post_id, 'title': title})}

def get_post(event, context):
    table = dynamodb.Table(POSTS_TABLE)

    result = table.get_item(
        Key={
            'postId': event['pathParameters']['id']
        }
    )

    response = {
        "statusCode": 200,
				"headers": header,
        "body": json.dumps(result['Item'])
    }

    return response

def list_post(event, context):
    table = dynamodb.Table(POSTS_TABLE)

  
    result = table.scan()

    
    response = {
        "statusCode": 200,
				"headers": header,
        "body": json.dumps(result['Items'])
    }

    return response

def update_post(event, context):
    data = json.loads(event['body'])
    if 'title' not in data:
        raise Exception("Couldn't update the post item.")
        return

    table = dynamodb.Table(POSTS_TABLE)

   
    result = table.update_item(
        Key={
            'postId': event['pathParameters']['id']
        },
        ExpressionAttributeValues={
          ':title': data['title']
        },
        UpdateExpression='SET title = :title',
        ReturnValues='ALL_NEW',
    )

   
    response = {
        "statusCode": 200,
				"headers": header,
        "body": json.dumps(result['Attributes'])
    }

    return response

def delete_post(event, context):
    table = dynamodb.Table(POSTS_TABLE)

   
    table.delete_item(
        Key={
            'postId': event['pathParameters']['id']
        }
    )

 
    response = {
        "statusCode": 200
    }

    return response

