import aws_cdk as cdk
import aws_cdk.assertions as assertions
from api_gateway_lambda.api_gateway_lambda_stack import ApiGatewayLambdaStack

def test_lambda_function_created():
    app = cdk.App()
    stack = ApiGatewayLambdaStack(app, "ApiGatewayLambdaStack")
    template = assertions.Template.from_stack(stack)
    
    # Assert that the Lambda function is created
    template.resource_count_is("AWS::Lambda::Function", 1)

def test_api_gateway_created():
    app = cdk.App()
    stack = ApiGatewayLambdaStack(app, "ApiGatewayLambdaStack")
    template = assertions.Template.from_stack(stack)
    
    # Assert that the API Gateway is created
    template.resource_count_is("AWS::ApiGateway::RestApi", 1)
    
    # Assert that we have methods defined
    template.resource_count_is("AWS::ApiGateway::Method", 2)  # GET and POST methods