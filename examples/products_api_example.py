# products_api_example.py
# 
# このファイルは、API Gateway と Lambda を使用して製品 API を実装する例を示しています。
# 実際のプロジェクトに統合する場合は、適切に修正してください。

# CDK スタックの更新例（api_gateway_lambda_stack.py に追加）
"""
# 製品 API のリソースを追加
products_resource = api.root.add_resource("products")
products_resource.add_method("GET", lambda_integration)
products_resource.add_method("POST", lambda_integration)

# 製品詳細のリソースを追加（パスパラメータ使用）
product_detail_resource = products_resource.add_resource("{productId}")
product_detail_resource.add_method("GET", lambda_integration)
product_detail_resource.add_method("PUT", lambda_integration)
product_detail_resource.add_method("DELETE", lambda_integration)

# 製品カテゴリのリソースを追加
categories_resource = api.root.add_resource("categories")
categories_resource.add_method("GET", lambda_integration)
"""

# Lambda ハンドラーの更新例（api_handler.py に追加）
import json
import logging
import datetime
import re

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    """
    Lambda function handler for API Gateway requests.
    """
    logger.info('Event: %s', event)
    
    http_method = event.get('httpMethod', '')
    path = event.get('path', '')
    
    # 現在の時刻を取得
    current_time = datetime.datetime.now().isoformat()
    
    # パスとメソッドに基づいて処理を分岐
    if path == '/api':
        return handle_api_endpoint(event, current_time)
    elif path == '/products':
        return handle_products_endpoint(event, current_time)
    elif re.match(r'^/products/[^/]+$', path):
        return handle_product_detail_endpoint(event, current_time)
    elif path == '/categories':
        return handle_categories_endpoint(event, current_time)
    else:
        response_body = {
            'message': f'Unsupported path: {path}',
            'timestamp': current_time
        }
        return create_response(404, response_body)

def handle_products_endpoint(event, current_time):
    """製品一覧 /products エンドポイントの処理"""
    http_method = event.get('httpMethod', '')
    
    if http_method == 'GET':
        # クエリパラメータの取得
        query_params = event.get('queryStringParameters', {}) or {}
        category = query_params.get('category')
        
        # 製品一覧を返す（実際のアプリケーションではデータベースから取得）
        products = [
            {'id': '1', 'name': 'Product 1', 'price': 1000, 'category': 'electronics'},
            {'id': '2', 'name': 'Product 2', 'price': 2000, 'category': 'books'},
            {'id': '3', 'name': 'Product 3', 'price': 3000, 'category': 'electronics'}
        ]
        
        # カテゴリでフィルタリング
        if category:
            products = [p for p in products if p.get('category') == category]
        
        response_body = {
            'products': products,
            'count': len(products),
            'timestamp': current_time
        }
        return create_response(200, response_body)
    
    elif http_method == 'POST':
        # 新しい製品を作成（実際のアプリケーションではデータベースに保存）
        try:
            body = json.loads(event.get('body', '{}'))
            
            # 必須フィールドの検証
            required_fields = ['name', 'price', 'category']
            for field in required_fields:
                if field not in body:
                    return create_response(400, {
                        'message': f'Missing required field: {field}',
                        'timestamp': current_time
                    })
            
            # 新しい製品 ID を生成（実際のアプリケーションではデータベースが生成）
            new_product = body.copy()
            new_product['id'] = '123'  # 仮の ID
            
            response_body = {
                'message': 'Product created successfully',
                'product': new_product,
                'timestamp': current_time
            }
            return create_response(201, response_body)
        
        except json.JSONDecodeError:
            response_body = {
                'message': 'Invalid JSON in request body',
                'timestamp': current_time
            }
            return create_response(400, response_body)
    
    else:
        response_body = {
            'message': f'Unsupported method: {http_method}',
            'timestamp': current_time
        }
        return create_response(405, response_body)

def handle_product_detail_endpoint(event, current_time):
    """製品詳細 /products/{productId} エンドポイントの処理"""
    http_method = event.get('httpMethod', '')
    path = event.get('path', '')
    
    # パスから製品 ID を抽出
    product_id = path.split('/')[-1]
    
    if http_method == 'GET':
        # 特定の製品情報を返す（実際のアプリケーションではデータベースから取得）
        product = {
            'id': product_id,
            'name': f'Product {product_id}',
            'price': 1000,
            'description': 'This is a sample product',
            'category': 'electronics'
        }
        
        response_body = {
            'product': product,
            'timestamp': current_time
        }
        return create_response(200, response_body)
    
    elif http_method == 'PUT':
        # 製品情報を更新
        try:
            body = json.loads(event.get('body', '{}'))
            
            # 更新された製品情報（実際のアプリケーションではデータベースを更新）
            updated_product = {
                'id': product_id,
                'name': body.get('name', f'Product {product_id}'),
                'price': body.get('price', 1000),
                'description': body.get('description', 'This is a sample product'),
                'category': body.get('category', 'electronics')
            }
            
            response_body = {
                'message': f'Product {product_id} updated successfully',
                'product': updated_product,
                'timestamp': current_time
            }
            return create_response(200, response_body)
        
        except json.JSONDecodeError:
            response_body = {
                'message': 'Invalid JSON in request body',
                'timestamp': current_time
            }
            return create_response(400, response_body)
    
    elif http_method == 'DELETE':
        # 製品を削除（実際のアプリケーションではデータベースから削除）
        response_body = {
            'message': f'Product {product_id} deleted successfully',
            'timestamp': current_time
        }
        return create_response(200, response_body)
    
    else:
        response_body = {
            'message': f'Unsupported method: {http_method}',
            'timestamp': current_time
        }
        return create_response(405, response_body)

def handle_categories_endpoint(event, current_time):
    """カテゴリ一覧 /categories エンドポイントの処理"""
    http_method = event.get('httpMethod', '')
    
    if http_method == 'GET':
        # カテゴリ一覧を返す（実際のアプリケーションではデータベースから取得）
        categories = [
            {'id': '1', 'name': 'electronics', 'description': 'Electronic devices and gadgets'},
            {'id': '2', 'name': 'books', 'description': 'Books and publications'},
            {'id': '3', 'name': 'clothing', 'description': 'Apparel and fashion items'}
        ]
        
        response_body = {
            'categories': categories,
            'timestamp': current_time
        }
        return create_response(200, response_body)
    
    else:
        response_body = {
            'message': f'Unsupported method: {http_method}',
            'timestamp': current_time
        }
        return create_response(405, response_body)

def create_response(status_code, body):
    """レスポンスを生成するヘルパー関数"""
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'  # CORS サポート
        },
        'body': json.dumps(body)
    }

# テスト例（tests/unit/test_products_api.py として追加）
"""
import json
import sys
import os
import pytest

# Lambda ディレクトリをパスに追加
sys.path.append(os.path.join(os.path.dirname(__file__), '../../lambda'))

from api_handler import handler

def test_get_products():
    # 製品一覧取得のテスト
    event = {
        'httpMethod': 'GET',
        'path': '/products',
        'headers': {},
        'queryStringParameters': None,
        'body': None
    }
    
    response = handler(event, None)
    
    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert 'products' in body
    assert isinstance(body['products'], list)

def test_get_products_with_category_filter():
    # カテゴリフィルタ付きの製品一覧取得テスト
    event = {
        'httpMethod': 'GET',
        'path': '/products',
        'headers': {},
        'queryStringParameters': {'category': 'electronics'},
        'body': None
    }
    
    response = handler(event, None)
    
    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert 'products' in body
    assert all(p['category'] == 'electronics' for p in body['products'])

def test_get_product_detail():
    # 製品詳細取得のテスト
    event = {
        'httpMethod': 'GET',
        'path': '/products/123',
        'headers': {},
        'queryStringParameters': None,
        'pathParameters': {'productId': '123'},
        'body': None
    }
    
    response = handler(event, None)
    
    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert 'product' in body
    assert body['product']['id'] == '123'

def test_create_product():
    # 製品作成のテスト
    new_product = {
        'name': 'New Product',
        'price': 1500,
        'category': 'books'
    }
    
    event = {
        'httpMethod': 'POST',
        'path': '/products',
        'headers': {'Content-Type': 'application/json'},
        'queryStringParameters': None,
        'body': json.dumps(new_product)
    }
    
    response = handler(event, None)
    
    assert response['statusCode'] == 201
    body = json.loads(response['body'])
    assert 'product' in body
    assert body['product']['name'] == 'New Product'
    assert body['product']['price'] == 1500
    assert body['product']['category'] == 'books'
"""