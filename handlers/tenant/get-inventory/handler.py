import json

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
        return respond( 4000, {
            'message': 'No body'
        })
    
    parsed_body = json.loads(body)
    try:
        return respond(200, { 
            'message': 'Hello'
        })
        # response = stripe.PaymentIntent.create_payment_intent()
    except:
        return respond(500, { 
            'message': "Error" 
        })