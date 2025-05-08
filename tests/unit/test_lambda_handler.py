import json
import sys
import os
import pytest

# Add the lambda directory to the path so we can import the handler
sys.path.append(os.path.join(os.path.dirname(__file__), '../../lambda'))

from api_handler import handler

def test_get_request():
    # Create a mock GET event
    event = {
        'httpMethod': 'GET',
        'path': '/api',
        'headers': {},
        'queryStringParameters': None,
        'body': None
    }
    
    # Call the handler
    response = handler(event, None)
    
    # Assert the response
    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert 'message' in body
    assert body['message'] == 'Hello from Lambda!'
    assert 'timestamp' in body

def test_post_request():
    # Create a mock POST event with a JSON body
    test_data = {'name': 'Test User', 'message': 'Hello API'}
    event = {
        'httpMethod': 'POST',
        'path': '/api',
        'headers': {'Content-Type': 'application/json'},
        'queryStringParameters': None,
        'body': json.dumps(test_data)
    }
    
    # Call the handler
    response = handler(event, None)
    
    # Assert the response
    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert 'message' in body
    assert body['message'] == 'Data received successfully'
    assert 'received_data' in body
    assert body['received_data'] == test_data
    assert 'timestamp' in body

def test_unsupported_method():
    # Create a mock event with an unsupported method
    event = {
        'httpMethod': 'PUT',
        'path': '/api',
        'headers': {},
        'queryStringParameters': None,
        'body': None
    }
    
    # Call the handler
    response = handler(event, None)
    
    # Assert the response
    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert 'message' in body
    assert 'Unsupported method: PUT' in body['message']
    assert 'timestamp' in body