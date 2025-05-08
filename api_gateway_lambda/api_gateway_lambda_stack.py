from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    CfnOutput
)
from constructs import Construct

class ApiGatewayLambdaStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Define Lambda function
        lambda_function = _lambda.Function(
            self, "ApiHandler",
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset("lambda"),
            handler="api_handler.handler",
        )

        # Define API Gateway
        api = apigw.RestApi(
            self, "ApiGateway",
            rest_api_name="API Gateway Lambda Service",
            description="This service serves as an API Gateway for Lambda integration."
        )

        # Create an API Gateway integration with the Lambda function
        lambda_integration = apigw.LambdaIntegration(
            lambda_function,
            request_templates={"application/json": '{ "statusCode": "200" }'}
        )

        # Define API resources and methods
        api_resource = api.root.add_resource("api")
        
        # GET method
        api_resource.add_method("GET", lambda_integration)
        
        # POST method
        api_resource.add_method("POST", lambda_integration)

        # Output the API Gateway URL
        CfnOutput(
            self, "ApiUrl",
            value=f"{api.url}api"
        )