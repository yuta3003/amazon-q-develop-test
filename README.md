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
├── docs/                      # ドキュメント
│   ├── README.md              # 業務フローと API 拡張ガイド
│   └── adding_endpoints.md    # API エンドポイント追加の詳細ガイド
├── examples/                  # 実装例
│   ├── products_api_example.py        # 製品 API の実装例
│   └── test_products_api_example.py   # 製品 API のテスト例
├── requirements.txt           # Python 依存関係
└── setup.py                   # セットアップスクリプト
```

## 機能

- API Gateway を通じて `/api` エンドポイントを公開
- GET リクエスト: 現在の時刻とメッセージを返す
- POST リクエスト: 送信されたデータを受け取り、確認メッセージを返す

## ドキュメント

詳細なドキュメントは `docs` ディレクトリにあります：

- [業務フローと API 拡張ガイド](docs/README.md) - Mermaid を使用した業務フロー図と API の概要
- [API エンドポイント追加ガイド](docs/adding_endpoints.md) - 新しい API エンドポイントを追加する方法の詳細

また、`examples` ディレクトリには、新しい API エンドポイントを追加するための実装例があります：

- [製品 API の実装例](examples/products_api_example.py)
- [製品 API のテスト例](examples/test_products_api_example.py)

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
