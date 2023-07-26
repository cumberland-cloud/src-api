import json

import stripe

def lambda_handler(event, context):
    body = event.get('body', None)

    if body is not None:
        parsed_body = json.loads(body)
        try:
            response = stripe.PaymentIntent.create_payment_intent()
        except:
            response, status = "Error", 500
        
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