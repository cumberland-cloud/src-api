import json

def lambda_handler(event, context):
    body = event.get('body', None)

    if body is not None:
        response = json.loads(body)
    else:
        response = {
          'message' : 'Hello from lambda!'
        }

    return {
          "isBase64Encoded": False,
          "statusCode": 200,
          "headers": {
              "Access-Control-Allow-Headers": "Content-Type",
              "Allow": "OPTIONS, POST",
              "Access-Control-Allow-Origin": "*",
              "Access-Control-Allow-Methods": "OPTIONS,POST",
              "Content-Type": "application/json"
          },
          "body": json.dumps(response)
    } 