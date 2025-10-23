# 進捗データ管理API ドキュメント

## 概要

このAPIは、キッチンゲームの進捗データを管理するためのRESTful APIです。

## 機能

- 進捗データの取得
- 進捗データの保存
- 進捗データのリセット
- DeliveryManagerとの自動統合

## セットアップ

### 必要なパッケージのインストール

```bash
pip install -r requirements.txt
```

### サーバーの起動

```bash
python3 main.py
```

サーバーはデフォルトで `http://localhost:5000` で起動します。

## APIエンドポイント

### 1. ルート - API情報取得

**エンドポイント:** `GET /`

**説明:** API の概要と利用可能なエンドポイントを取得します。

**レスポンス例:**
```json
{
  "message": "進捗データ管理API",
  "endpoints": {
    "GET /api/progress": "進捗データを取得",
    "POST /api/progress": "進捗データを保存",
    "POST /api/progress/reset": "進捗データをリセット"
  }
}
```

### 2. 進捗データ取得

**エンドポイント:** `GET /api/progress`

**説明:** 現在の進捗データを取得します。

**レスポンス例:**
```json
{
  "success": true,
  "data": {
    "successful_recipes": 10,
    "total_deliveries": 15,
    "failed_deliveries": 5,
    "last_updated": "2025-10-23T07:56:00.520543"
  }
}
```

**フィールド説明:**
- `successful_recipes`: 成功したレシピ数
- `total_deliveries`: 合計配達数
- `failed_deliveries`: 失敗した配達数
- `last_updated`: 最終更新日時（ISO 8601形式）

### 3. 進捗データ保存

**エンドポイント:** `POST /api/progress`

**説明:** 進捗データを保存します。

**リクエストボディ:**
```json
{
  "successful_recipes": 10,
  "total_deliveries": 15,
  "failed_deliveries": 5
}
```

**レスポンス例:**
```json
{
  "success": true,
  "message": "進捗データを保存しました",
  "data": {
    "successful_recipes": 10,
    "total_deliveries": 15,
    "failed_deliveries": 5,
    "last_updated": "2025-10-23T07:56:00.520543"
  }
}
```

### 4. 進捗データリセット

**エンドポイント:** `POST /api/progress/reset`

**説明:** 進捗データをすべてリセットします。

**レスポンス例:**
```json
{
  "success": true,
  "message": "進捗データをリセットしました",
  "data": {
    "successful_recipes": 0,
    "total_deliveries": 0,
    "failed_deliveries": 0,
    "last_updated": "2025-10-23T07:56:00.516422"
  }
}
```

## 使用例

### curlを使用した例

```bash
# 進捗データを取得
curl http://localhost:5000/api/progress

# 進捗データを保存
curl -X POST http://localhost:5000/api/progress \
  -H "Content-Type: application/json" \
  -d '{"successful_recipes": 10, "total_deliveries": 15, "failed_deliveries": 5}'

# 進捗データをリセット
curl -X POST http://localhost:5000/api/progress/reset
```

### Pythonを使用した例

```python
import requests

# 進捗データを取得
response = requests.get('http://localhost:5000/api/progress')
data = response.json()
print(data)

# 進捗データを保存
response = requests.post(
    'http://localhost:5000/api/progress',
    json={
        'successful_recipes': 10,
        'total_deliveries': 15,
        'failed_deliveries': 5
    }
)
data = response.json()
print(data)
```

## DeliveryManagerとの統合

`progress_manager.py` は `deliverManager.py` と統合されており、レシピの配達が成功または失敗すると自動的に進捗データが更新されます。

- **成功時**: `update_successful_recipes()` が自動的に呼ばれます
- **失敗時**: `update_failed_deliveries()` が自動的に呼ばれます

## データの永続化

進捗データは `progress_data.json` ファイルに保存されます。このファイルはサーバーの再起動後も保持されます。

## テスト

### 統合テストの実行

```bash
python3 test_integration.py
```

DeliveryManagerとProgressManagerの統合をテストします。

### APIテストの実行

```bash
# サーバーを起動
python3 main.py

# 別のターミナルでテストを実行
python3 test_api.py
```

すべてのAPIエンドポイントの動作をテストします。

## エラーハンドリング

APIエラーが発生した場合、以下の形式でレスポンスが返されます：

```json
{
  "success": false,
  "error": "エラーメッセージ"
}
```

適切なHTTPステータスコード（400, 500など）が返されます。

## 技術スタック

- **Flask 3.0.0**: Webフレームワーク
- **Python 3.11**: プログラミング言語
- **JSON**: データ保存形式

## ファイル構成

- `main.py`: Flask APIサーバー
- `progress_manager.py`: 進捗データ管理クラス
- `deliverManager.py`: 配達管理クラス（統合済み）
- `test_integration.py`: 統合テスト
- `test_api.py`: APIテスト
- `requirements.txt`: 依存パッケージ
- `progress_data.json`: 進捗データファイル（自動生成）
