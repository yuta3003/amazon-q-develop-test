import json
import logging
import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    """
    Lambda function handler for API Gateway requests.
    
    Parameters:
    event (dict): API Gateway Lambda Proxy Input Format
    context (object): Lambda Context runtime methods and attributes
    
    Returns:
    dict: API Gateway Lambda Proxy Output Format
    """
    logger.info('Event: %s', event)
    
    http_method = event.get('httpMethod', '')
    
    # Get current time in ISO format
    current_time = datetime.datetime.now().isoformat()
    
    if http_method == 'GET':
        response_body = {
            'message': 'Hello from Lambda!',
            'timestamp': current_time
        }
    elif http_method == 'POST':
        # Parse the request body if it exists
        try:
            body = json.loads(event.get('body', '{}'))
            response_body = {
                'message': 'Data received successfully',
                'received_data': body,
                'timestamp': current_time
            }
        except json.JSONDecodeError:
            response_body = {
                'message': 'Invalid JSON in request body',
                'timestamp': current_time
            }
    else:
        response_body = {
            'message': f'Unsupported method: {http_method}',
            'timestamp': current_time
        }
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'  # For CORS support
        },
        'body': json.dumps(response_body)
    }