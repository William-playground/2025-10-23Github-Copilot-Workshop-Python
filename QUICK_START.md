# クイックスタートガイド

## 準備

### 1. 依存パッケージのインストール
```bash
pip install -r requirements.txt
```

## 使い方

### サーバー起動
```bash
python3 main.py
```

サーバーは `http://localhost:5000` で起動します。

### API使用例

#### 進捗データを取得
```bash
curl http://localhost:5000/api/progress
```

#### 進捗データを保存
```bash
curl -X POST http://localhost:5000/api/progress \
  -H "Content-Type: application/json" \
  -d '{
    "successful_recipes": 10,
    "total_deliveries": 15,
    "failed_deliveries": 5
  }'
```

#### 進捗データをリセット
```bash
curl -X POST http://localhost:5000/api/progress/reset
```

## テスト

### 統合テスト
```bash
python3 test_integration.py
```

### APIテスト
```bash
# 別のターミナルでサーバーを起動
python3 main.py

# テスト実行
python3 test_api.py
```

## プログラムから使用

```python
from progress_manager import ProgressManager

# インスタンス取得
pm = ProgressManager.get_instance()

# 進捗データ保存
result = pm.save_progress(
    successful_recipes=10,
    total_deliveries=15,
    failed_deliveries=5
)

# 進捗データ取得
progress = pm.get_progress()
print(progress)

# 成功レシピをインクリメント
pm.update_successful_recipes()

# 失敗配達をインクリメント
pm.update_failed_deliveries()
```

## DeliveryManager統合

DeliveryManagerを使用すると、進捗は自動的に追跡されます：

```python
from deliverManager import DeliveryManager, RecipeListSO

# DeliveryManagerを使用
delivery_manager = DeliveryManager.get_instance(recipe_list)

# レシピ配達（成功・失敗が自動追跡される）
delivery_manager.deliver_recipe(plate)
```

## 詳細ドキュメント

- 完全なAPIドキュメント: [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
- 実装の詳細: [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)
