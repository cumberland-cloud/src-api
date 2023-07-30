from typing import Dict, List, Union

import json
import os
import requests
import jwt

from jwt.algorithms import RSAAlgorithm

ACCOUNT_ID = os.environ['ACCOUNT_ID']
API_ID = os.environ['API_ID']
USERPOOL_ID = os.environ['USERPOOL_ID']
CLIENT_ID = os.environ['CLIENT_ID']
REGION = os.environ['REGION']
GROUP = os.environ.setdefault('GROUP', None)

def key_url() -> str:
    return 'https://cognito-idp.{}.amazonawse.com/{}/.well-known/jwks.json'.format(REGION, USERPOOL_ID)

def lambda_handler(event: dict, context: dict):
    token = event['authorizationToken'].split(' ')[-1]
    header = jwt.get_unverified_header(token)

    keys = requests.get(key_url()).json()['keys']
    kid = header['kid']
    jwk = find_key(keys, kid)

    if jwk is None:
        return policy(None, True)

    try:
        public_key = RSAAlgorithm.from_jwk(json.dumps(jwk))
        decoded = decode_token(token, public_key)

        if GROUP is None:
            return policy(decoded['cognito:username'], False)

        if GROUP in decoded['cognito:groups']:
            return policy(decoded['cognito:username'], False)

        return policy(decoded['cognito:username'], True)

    except Exception as e:
        print(e)
        return policy(None, True)

def policy(principal: str, deny: bool) -> dict:
    return {
        "principalId": principal,
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [{
                "Action": "execute-api:Invoke",
                "Effect": "Deny" if deny else "Allow",
                "Resource": f"arn:aws:execute-api:{REGION}:{ACCOUNT_ID}:{API_ID}/*"
            }]
        }
    }

def find_key(keys: List[Dict], kid: str) -> Union[dict,None]:
    for key in keys:
        if key['kid'] == kid:
            return key
    return None

def decode_token(token: str, publicKey: str)->dict:
    return jwt.decode(token, publicKey, algorithms=['RS256'], audience=CLIENT_ID)
