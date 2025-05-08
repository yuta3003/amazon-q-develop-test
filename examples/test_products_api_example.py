# test_products_api_example.py
#
# このファイルは、製品 API のテスト例を示しています。
# 実際のプロジェクトに統合する場合は、tests/unit/ ディレクトリに配置し、適切に修正してください。

import json
import sys
import os
import pytest

# 製品 API の実装をインポート
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))
from products_api_example import handler, handle_products_endpoint, handle_product_detail_endpoint, handle_categories_endpoint

def test_get_products():
    """製品一覧取得のテスト"""
    event = {
        'httpMethod': 'GET',
        'path': '/products',
        'headers': {},
        'queryStringParameters': None,
        'body': None
    }
    
    # ハンドラー関数を直接呼び出し
    response = handle_products_endpoint(event, "2023-01-01T00:00:00")
    
    # レスポンスの検証
    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert 'products' in body
    assert isinstance(body['products'], list)
    assert len(body['products']) > 0

def test_get_products_with_category_filter():
    """カテゴリフィルタ付きの製品一覧取得テスト"""
    event = {
        'httpMethod': 'GET',
        'path': '/products',
        'headers': {},
        'queryStringParameters': {'category': 'electronics'},
        'body': None
    }
    
    # ハンドラー関数を直接呼び出し
    response = handle_products_endpoint(event, "2023-01-01T00:00:00")
    
    # レスポンスの検証
    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert 'products' in body
    assert all(p['category'] == 'electronics' for p in body['products'])

def test_create_product():
    """製品作成のテスト"""
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
    
    # ハンドラー関数を直接呼び出し
    response = handle_products_endpoint(event, "2023-01-01T00:00:00")
    
    # レスポンスの検証
    assert response['statusCode'] == 201
    body = json.loads(response['body'])
    assert 'product' in body
    assert body['product']['name'] == 'New Product'
    assert body['product']['price'] == 1500
    assert body['product']['category'] == 'books'

def test_create_product_missing_field():
    """必須フィールドが欠けている場合のテスト"""
    incomplete_product = {
        'name': 'Incomplete Product',
        # price フィールドが欠けている
        'category': 'books'
    }
    
    event = {
        'httpMethod': 'POST',
        'path': '/products',
        'headers': {'Content-Type': 'application/json'},
        'queryStringParameters': None,
        'body': json.dumps(incomplete_product)
    }
    
    # ハンドラー関数を直接呼び出し
    response = handle_products_endpoint(event, "2023-01-01T00:00:00")
    
    # レスポンスの検証
    assert response['statusCode'] == 400
    body = json.loads(response['body'])
    assert 'message' in body
    assert 'Missing required field' in body['message']

def test_get_product_detail():
    """製品詳細取得のテスト"""
    event = {
        'httpMethod': 'GET',
        'path': '/products/123',
        'headers': {},
        'queryStringParameters': None,
        'pathParameters': {'productId': '123'},
        'body': None
    }
    
    # ハンドラー関数を直接呼び出し
    response = handle_product_detail_endpoint(event, "2023-01-01T00:00:00")
    
    # レスポンスの検証
    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert 'product' in body
    assert body['product']['id'] == '123'

def test_update_product():
    """製品更新のテスト"""
    update_data = {
        'name': 'Updated Product',
        'price': 2500
    }
    
    event = {
        'httpMethod': 'PUT',
        'path': '/products/123',
        'headers': {'Content-Type': 'application/json'},
        'queryStringParameters': None,
        'pathParameters': {'productId': '123'},
        'body': json.dumps(update_data)
    }
    
    # ハンドラー関数を直接呼び出し
    response = handle_product_detail_endpoint(event, "2023-01-01T00:00:00")
    
    # レスポンスの検証
    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert 'product' in body
    assert body['product']['id'] == '123'
    assert body['product']['name'] == 'Updated Product'
    assert body['product']['price'] == 2500

def test_delete_product():
    """製品削除のテスト"""
    event = {
        'httpMethod': 'DELETE',
        'path': '/products/123',
        'headers': {},
        'queryStringParameters': None,
        'pathParameters': {'productId': '123'},
        'body': None
    }
    
    # ハンドラー関数を直接呼び出し
    response = handle_product_detail_endpoint(event, "2023-01-01T00:00:00")
    
    # レスポンスの検証
    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert 'message' in body
    assert 'deleted successfully' in body['message']

def test_get_categories():
    """カテゴリ一覧取得のテスト"""
    event = {
        'httpMethod': 'GET',
        'path': '/categories',
        'headers': {},
        'queryStringParameters': None,
        'body': None
    }
    
    # ハンドラー関数を直接呼び出し
    response = handle_categories_endpoint(event, "2023-01-01T00:00:00")
    
    # レスポンスの検証
    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert 'categories' in body
    assert isinstance(body['categories'], list)
    assert len(body['categories']) > 0

def test_unsupported_method():
    """未対応メソッドのテスト"""
    event = {
        'httpMethod': 'PATCH',
        'path': '/products',
        'headers': {},
        'queryStringParameters': None,
        'body': None
    }
    
    # ハンドラー関数を直接呼び出し
    response = handle_products_endpoint(event, "2023-01-01T00:00:00")
    
    # レスポンスの検証
    assert response['statusCode'] == 405
    body = json.loads(response['body'])
    assert 'message' in body
    assert 'Unsupported method' in body['message']

# メインハンドラーのテスト
def test_main_handler_routing():
    """メインハンドラーのルーティングテスト"""
    # 製品一覧へのリクエスト
    products_event = {
        'httpMethod': 'GET',
        'path': '/products',
        'headers': {},
        'queryStringParameters': None,
        'body': None
    }
    
    response = handler(products_event, None)
    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert 'products' in body
    
    # 製品詳細へのリクエスト
    product_detail_event = {
        'httpMethod': 'GET',
        'path': '/products/123',
        'headers': {},
        'queryStringParameters': None,
        'body': None
    }
    
    response = handler(product_detail_event, None)
    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert 'product' in body
    
    # カテゴリ一覧へのリクエスト
    categories_event = {
        'httpMethod': 'GET',
        'path': '/categories',
        'headers': {},
        'queryStringParameters': None,
        'body': None
    }
    
    response = handler(categories_event, None)
    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert 'categories' in body
    
    # 未対応パスへのリクエスト
    unknown_path_event = {
        'httpMethod': 'GET',
        'path': '/unknown',
        'headers': {},
        'queryStringParameters': None,
        'body': None
    }
    
    response = handler(unknown_path_event, None)
    assert response['statusCode'] == 404
    body = json.loads(response['body'])
    assert 'message' in body
    assert 'Unsupported path' in body['message']