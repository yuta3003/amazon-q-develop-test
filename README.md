# API Gateway と Lambda を使用した API の構築

このプロジェクトは AWS CDK を使用して、Amazon API Gateway と AWS Lambda による REST API を構築します。Lambda 関数は Python で実装されています。

## プロジェクト構成

```
.
├── README.md                  # このファイル
├── app.py                     # CDK アプリケーションのエントリーポイント
├── api_gateway_lambda/        # CDK スタック定義
│   ├── __init__.py
│   └── api_gateway_lambda_stack.py
├── lambda/                    # Lambda 関数のコード
│   └── api_handler.py
├── tests/                     # テストコード
│   └── unit/
│       ├── test_api_gateway_lambda_stack.py
│       └── test_lambda_handler.py
├── requirements.txt           # Python 依存関係
└── setup.py                   # セットアップスクリプト
```

## 機能

- API Gateway を通じて `/api` エンドポイントを公開
- GET リクエスト: 現在の時刻とメッセージを返す
- POST リクエスト: 送信されたデータを受け取り、確認メッセージを返す

## デプロイ方法

### 前提条件

- AWS CLI がインストールされ、設定済み
- Python 3.6 以上
- AWS CDK v2 がインストール済み

### セットアップ手順

1. 依存関係のインストール:

```bash
pip install -r requirements.txt
```

2. CDK の初期化 (初回のみ):

```bash
cdk bootstrap
```

3. デプロイ:

```bash
cdk deploy
```

デプロイが完了すると、API Gateway の URL が出力されます。

## テスト実行方法

単体テストを実行するには:

```bash
pytest
```

## API の使用方法

### GET リクエスト

```bash
curl https://your-api-id.execute-api.region.amazonaws.com/prod/api
```

### POST リクエスト

```bash
curl -X POST \
  https://your-api-id.execute-api.region.amazonaws.com/prod/api \
  -H 'Content-Type: application/json' \
  -d '{"name": "Test User", "message": "Hello API"}'
```

## クリーンアップ

リソースを削除するには:

```bash
cdk destroy
```
