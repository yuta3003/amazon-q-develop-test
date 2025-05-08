#!/usr/bin/env python3
import os
from aws_cdk import App

from api_gateway_lambda.api_gateway_lambda_stack import ApiGatewayLambdaStack

app = App()
ApiGatewayLambdaStack(app, "ApiGatewayLambdaStack")

app.synth()