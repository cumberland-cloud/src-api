# Authorize

This is a **AWS Lambda** function for authorizing requests to an **API Gateway** through a **Cognito Userpool**. This function will [decode a Cognito JWT token](https://aws.amazon.com/premiumsupport/knowledge-center/decode-verify-cognito-json-token/) in a request's `Authorization` header and then return [a policy statement](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-lambda-authorizer-output.html) to inform **API Gateway** whether or not the incoming request is authorized to access the resource.

See [documentation for more information on using a Lambda authorizer in an API Gateway](https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-use-lambda-authorizer.html).

The source code for this Lambda can be found [here](https://github.com/chinchalinchin/cumbercloud-lambdas/blob/master/lambdas/auth/authorize/lambda_function.py).

## Configuration

### Environment Variables

1. **ACCOUNT_ID**: Identification number for AWS account.

2. **API_ID**: Physical identification number for API Gateway REST API deployment.

3. **USERPOOL_ID**: Cognito Userpool identification number.

4. **CLIENT_ID**: Physicacl identification number for the Cognito Client. 

6. **REGION**: Region where the API gateway is hosted. 

7. **GROUP**: *Optional*. If `GROUP` is specified, the user associated with incoming request must belong to the specified group name, found in the `cognito:groups` property in the JWT payload. If the user does not belong to this group, request will be rejected. If `GROUP` is not specified, function will only validate the authenticity of the JWT.

### Lambda Execution Role