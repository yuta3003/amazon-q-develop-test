# API エンドポイント追加ガイド

このガイドでは、API Gateway と Lambda を使用したプロジェクトに新しいエンドポイントを追加する詳細な手順を説明します。

## 目次

1. [基本的な概念](#基本的な概念)
2. [新しいエンドポイントの追加手順](#新しいエンドポイントの追加手順)
3. [実装例：ユーザー情報 API](#実装例ユーザー情報-api)
4. [パスパラメータの使用](#パスパラメータの使用)
5. [クエリパラメータの使用](#クエリパラメータの使用)
6. [認証の追加](#認証の追加)
7. [テストの追加](#テストの追加)

## 基本的な概念

このプロジェクトでは、以下のコンポーネントが連携しています：

- **API Gateway**: HTTP リクエストを受け付け、Lambda 関数にイベントとして転送します
- **Lambda 関数**: リクエストを処理し、レスポンスを返します
- **CDK スタック**: インフラストラクチャをコードとして定義します

新しいエンドポイントを追加する場合、CDK スタックと Lambda ハンドラーの両方を更新する必要があります。

## 新しいエンドポイントの追加手順

### 1. CDK スタックの更新

`api_gateway_lambda/api_gateway_lambda_stack.py` ファイルを編集して、新しいリソース（エンドポイント）を追加します：

```python
# 既存のコード...

# API Gateway の定義
api = apigw.RestApi(
    self, "ApiGateway",
    rest_api_name="API Gateway Lambda Service",
    description="This service serves as an API Gateway for Lambda integration."
)

# Lambda 統合の設定
lambda_integration = apigw.LambdaIntegration(
    lambda_function,
    request_templates={"application/json": '{ "statusCode": "200" }'}
)

# 既存のエンドポイント
api_resource = api.root.add_resource("api")
api_resource.add_method("GET", lambda_integration)
api_resource.add_method("POST", lambda_integration)

# 新しいエンドポイントの追加
new_resource = api.root.add_resource("users")
new_resource.add_method("GET", lambda_integration)
new_resource.add_method("POST", lambda_integration)

# ネストされたリソースの追加
user_id_resource = new_resource.add_resource("{userId}")
user_id_resource.add_method("GET", lambda_integration)
user_id_resource.add_method("PUT", lambda_integration)
user_id_resource.add_method("DELETE", lambda_integration)
```

### 2. Lambda ハンドラーの更新

`lambda/api_handler.py` ファイルを編集して、新しいエンドポイントのロジックを実装します：

```python
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
    elif path == '/users':
        return handle_users_endpoint(event, current_time)
    elif re.match(r'^/users/[^/]+$', path):
        return handle_user_detail_endpoint(event, current_time)
    else:
        response_body = {
            'message': f'Unsupported path: {path}',
            'timestamp': current_time
        }
        return create_response(200, response_body)

def handle_api_endpoint(event, current_time):
    """既存の /api エンドポイントの処理"""
    http_method = event.get('httpMethod', '')
    
    if http_method == 'GET':
        response_body = {
            'message': 'Hello from Lambda!',
            'timestamp': current_time
        }
    elif http_method == 'POST':
        # リクエストボディの解析
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
    
    return create_response(200, response_body)

def handle_users_endpoint(event, current_time):
    """新しい /users エンドポイントの処理"""
    http_method = event.get('httpMethod', '')
    
    if http_method == 'GET':
        # ユーザー一覧を返す（実際のアプリケーションではデータベースから取得）
        users = [
            {'id': '1', 'name': 'User 1'},
            {'id': '2', 'name': 'User 2'},
            {'id': '3', 'name': 'User 3'}
        ]
        response_body = {
            'users': users,
            'timestamp': current_time
        }
        return create_response(200, response_body)
    elif http_method == 'POST':
        # 新しいユーザーを作成（実際のアプリケーションではデータベースに保存）
        try:
            body = json.loads(event.get('body', '{}'))
            # ここでユーザーを作成するロジックを実装
            response_body = {
                'message': 'User created successfully',
                'user': body,
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

def handle_user_detail_endpoint(event, current_time):
    """ユーザー詳細 /users/{userId} エンドポイントの処理"""
    http_method = event.get('httpMethod', '')
    path = event.get('path', '')
    
    # パスからユーザーIDを抽出
    user_id = path.split('/')[-1]
    
    if http_method == 'GET':
        # 特定のユーザー情報を返す（実際のアプリケーションではデータベースから取得）
        user = {'id': user_id, 'name': f'User {user_id}', 'email': f'user{user_id}@example.com'}
        response_body = {
            'user': user,
            'timestamp': current_time
        }
        return create_response(200, response_body)
    elif http_method == 'PUT':
        # ユーザー情報を更新
        try:
            body = json.loads(event.get('body', '{}'))
            # ここでユーザーを更新するロジックを実装
            response_body = {
                'message': f'User {user_id} updated successfully',
                'user': body,
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
        # ユーザーを削除
        response_body = {
            'message': f'User {user_id} deleted successfully',
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

## 実装例：ユーザー情報 API

上記のコード例では、以下のエンドポイントを実装しています：

1. `GET /users` - ユーザー一覧を取得
2. `POST /users` - 新しいユーザーを作成
3. `GET /users/{userId}` - 特定のユーザー情報を取得
4. `PUT /users/{userId}` - ユーザー情報を更新
5. `DELETE /users/{userId}` - ユーザーを削除

## パスパラメータの使用

API Gateway では、パスパラメータを使用して動的なエンドポイントを作成できます：

```python
# CDK スタックでのパスパラメータの定義
user_resource = api.root.add_resource("users")
user_id_resource = user_resource.add_resource("{userId}")  # パスパラメータ
```

Lambda 関数では、パスパラメータは以下のように取得できます：

```python
# パスパラメータの取得
path_parameters = event.get('pathParameters', {})
user_id = path_parameters.get('userId')

# または正規表現を使用してパスから抽出
path = event.get('path', '')
match = re.match(r'^/users/([^/]+)$', path)
if match:
    user_id = match.group(1)
```

## クエリパラメータの使用

クエリパラメータを使用すると、フィルタリングやページネーションなどの機能を実装できます：

```python
def handle_users_endpoint(event, current_time):
    http_method = event.get('httpMethod', '')
    
    if http_method == 'GET':
        # クエリパラメータの取得
        query_params = event.get('queryStringParameters', {}) or {}
        limit = int(query_params.get('limit', 10))
        page = int(query_params.get('page', 1))
        
        # フィルタリングやページネーションのロジックを実装
        users = [
            {'id': '1', 'name': 'User 1'},
            {'id': '2', 'name': 'User 2'},
            {'id': '3', 'name': 'User 3'}
        ]
        
        # ページネーション処理（簡易的な例）
        start_idx = (page - 1) * limit
        end_idx = start_idx + limit
        paginated_users = users[start_idx:end_idx]
        
        response_body = {
            'users': paginated_users,
            'page': page,
            'limit': limit,
            'total': len(users),
            'timestamp': current_time
        }
        return create_response(200, response_body)
    # 他のメソッド処理...
```

## 認証の追加

API Gateway に認証を追加するには、以下のような方法があります：

### 1. API キー認証

```python
# CDK スタックでの API キー認証の設定
api = apigw.RestApi(
    self, "ApiGateway",
    rest_api_name="API Gateway Lambda Service",
    description="This service serves as an API Gateway for Lambda integration.",
    api_key_source_type=apigw.ApiKeySourceType.HEADER  # API キーをヘッダーから取得
)

# API キーの作成
api_key = api.add_api_key("ApiKey")

# 使用量プランの作成と API キーの関連付け
plan = api.add_usage_plan("UsagePlan",
    name="Standard",
    throttle=apigw.ThrottleSettings(
        rate_limit=10,
        burst_limit=2
    )
)
plan.add_api_key(api_key)
```

### 2. Cognito ユーザープールによる認証

```python
# CDK スタックでの Cognito 認証の設定
user_pool = cognito.UserPool(self, "UserPool")

authorizer = apigw.CognitoUserPoolsAuthorizer(self, "CognitoAuthorizer",
    cognito_user_pools=[user_pool]
)

# 認証が必要なエンドポイントの設定
users_resource = api.root.add_resource("users")
users_resource.add_method("GET", lambda_integration,
    authorizer=authorizer,
    authorization_type=apigw.AuthorizationType.COGNITO
)
```

## テストの追加

新しいエンドポイントを追加したら、テストも追加することをお勧めします。以下は、ユーザー API のテスト例です：

```python
def test_get_users():
    # ユーザー一覧取得のテスト
    event = {
        'httpMethod': 'GET',
        'path': '/users',
        'headers': {},
        'queryStringParameters': None,
        'body': None
    }
    
    response = handler(event, None)
    
    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert 'users' in body
    assert isinstance(body['users'], list)

def test_get_user_detail():
    # 特定のユーザー情報取得のテスト
    event = {
        'httpMethod': 'GET',
        'path': '/users/123',
        'headers': {},
        'queryStringParameters': None,
        'pathParameters': {'userId': '123'},
        'body': None
    }
    
    response = handler(event, None)
    
    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert 'user' in body
    assert body['user']['id'] == '123'
```