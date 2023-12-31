import boto3 
import json
import os

from botocore.exceptions import ClientError

CLIENT_ID = os.environ['CLIENT_ID']

def cognito_idp():
    return boto3.client('cognito-idp')

def respond(status: int, response: dict):
    return {
        "isBase64Encoded": False,
        "statusCode": status,
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Allow": "OPTIONS, POST",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST",
            "Content-Type": "application/json"
        },
        "body": json.dumps(response)
    } 

def handle(event, context):
    body = event.get('body', None)
    
    if body is None:
        return respond(400, {
          'message' : 'No body in request'
        })

    try:
        parsed_body = json.loads(body)
        response = cognito_idp().sign_up(
            UserName=parsed_body['username'],
            Password=parsed_body['password'],
            UserAttributes=[
                {
                    'Name': attribute,
                    'Value': parsed_body[attribute]
                } for attribute in ["email", "first_name", "last_name"]
            ],
            ClientId=CLIENT_ID,
        )
        return respond(200, response)

    except ClientError as e:
        return respond(500, e)