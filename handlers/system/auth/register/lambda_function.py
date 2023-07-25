import json
import os

import boto3 
from botocore.exceptions import ClientError

CLIENT_ID = os.environ['CLIENT_ID']

def cognito_idp():
    return boto3.client('cognito-idp')

def lambda_handler(event, context):
    body = event.get('body', None)

    if body is not None:
        parsed_body = json.loads(body)
        try:
            response = cognito_idp().sign_up(
                UserName=parsed_body['username'],
                Password=parsed_body['password'],
                UserAttributes=[
                    {
                        'Name': 'email',
                        'Value': parsed_body['email']
                    },
                    {
                        'Name': 'first_name',
                        'Value': parsed_body['first']
                    },
                    {
                        'Name': 'last_name',
                        'Value': parsed_body['last']
                    }
                ],
                ClientId=CLIENT_ID,
            )
            status = 200
        except ClientError as e:
            response, status = e, 500
        
    else:
        response = {
          'message' : 'No body in request'
        }
        status = 400

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