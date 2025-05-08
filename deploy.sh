#!/bin/bash
set -e

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running tests..."
pytest

echo "Deploying the CDK stack..."
cdk deploy

echo "Deployment completed successfully!"