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
        response = cognito_idp().initiate_auth(
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': parsed_body['username'],
                'PASSWORD': parsed_body['password']
            },
            ClientId=CLIENT_ID,
        )
        return respond(200, response)

    except ClientError as e:
        return respond(500, e)
