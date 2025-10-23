# データ管理抽象化システム

このドキュメントでは、データ管理の抽象化システムの使用方法について説明します。

## 概要

このシステムは、メモリベースとファイルベースのデータストレージを抽象化し、簡単に切り替えられるようにします。

### 主要コンポーネント

1. **IDataRepository** - データリポジトリの抽象インターフェース
2. **MemoryDataRepository** - メモリベースの実装
3. **FileDataRepository** - ファイルベース（JSON）の実装
4. **DataRepositoryFactory** - リポジトリのファクトリクラス
5. **Config** - アプリケーション設定管理

## 基本的な使い方

### 1. メモリベースストレージの使用

```python
from data_repository import DataRepositoryFactory

# メモリベースのリポジトリを作成
repo = DataRepositoryFactory.create("memory")

# データを保存
repo.save("user1", {"name": "太郎", "score": 100})

# データを読み込み
user_data = repo.load("user1")
print(user_data)  # {'name': '太郎', 'score': 100}

# データが存在するかチェック
if repo.exists("user1"):
    print("データが存在します")

# データを削除
repo.delete("user1")

# すべてのデータをクリア
repo.clear()
```

### 2. ファイルベースストレージの使用

```python
from data_repository import DataRepositoryFactory

# ファイルベースのリポジトリを作成
repo = DataRepositoryFactory.create("file", base_dir="./my_data")

# データを保存（./my_data/recipe1.json に保存される）
repo.save("recipe1", {
    "name": "サンドイッチ",
    "ingredients": ["パン", "レタス", "トマト"]
})

# データを読み込み
recipe = repo.load("recipe1")
print(recipe)

# データを削除
repo.delete("recipe1")

# すべてのデータファイルをクリア
repo.clear()
```

### 3. 設定ファイルを使用した切り替え

```python
from config import get_config

# 設定ファイルを作成
config = get_config()
config.set("storage_type", "file")  # または "memory"
config.set("data_dir", "./my_data")
config.save_to_file("./app_config.json")

# 設定ファイルから読み込み
from config import reset_config, get_config
reset_config()
config = get_config("./app_config.json")

print(f"ストレージタイプ: {config.storage_type}")
print(f"データディレクトリ: {config.data_dir}")
```

### 4. 環境変数を使用した切り替え

環境変数で設定を上書きできます：

```bash
# Linuxシェル
export STORAGE_TYPE=file
export DATA_DIR=./production_data
python main.py

# Windows PowerShell
$env:STORAGE_TYPE="file"
$env:DATA_DIR="./production_data"
python main.py
```

```python
from config import get_config
from data_repository import DataRepositoryFactory

# 環境変数から設定を読み込む
config = get_config()
repo = DataRepositoryFactory.create(
    config.storage_type,
    base_dir=config.data_dir
)
```

## DeliveryManagerとの統合

DeliveryManagerは自動的にデータリポジトリを使用してゲーム状態を保存します：

```python
from deliverManager import DeliveryManager, RecipeListSO
from data_repository import DataRepositoryFactory

# データリポジトリを作成
repo = DataRepositoryFactory.create("file", base_dir="./game_save")

# DeliveryManagerを初期化（リポジトリを指定）
recipe_list = RecipeListSO([...])
delivery_manager = DeliveryManager.get_instance(recipe_list, repo)

# レシピ配達時に自動的に状態が保存される
delivery_manager.deliver_recipe(plate)

# 明示的に状態を保存することも可能
delivery_manager.save_game_state()
```

## データ構造

### 保存される状態

```json
{
  "successful_recipes_amount": 5,
  "waiting_recipes": [
    {
      "name": "サンドイッチ",
      "ingredients": [
        {"name": "パン", "id": 1},
        {"name": "レタス", "id": 2},
        {"name": "トマト", "id": 3}
      ]
    }
  ]
}
```

## セキュリティ

### パストラバーサル保護

FileDataRepositoryは、パストラバーサル攻撃を防ぐため、キー名から `/` と `\` を自動的に除去します。

```python
repo = FileDataRepository(base_dir="./data")

# この保存は安全に処理される
repo.save("../../../etc/passwd", "malicious")
# 実際には ./data/.._.._.._etc_passwd.json に保存される
```

## テスト

テストを実行するには：

```bash
python test_data_repository.py
```

すべてのテストが成功すると、以下のようなメッセージが表示されます：

```
============================================================
データリポジトリのテスト実行
============================================================

テスト: MemoryDataRepository
  ✓ すべてのテストが成功

テスト: FileDataRepository
  ✓ すべてのテストが成功

...（省略）

============================================================
すべてのテストが成功しました！
============================================================
```

## 例

完全な動作例は以下のファイルを参照してください：

- `example_data_management.py` - メモリとファイルストレージの両方の使用例
- `data_repository.py` - 実装とシンプルな使用例
- `config.py` - 設定管理の使用例

## API リファレンス

### IDataRepository

すべてのデータリポジトリ実装が実装すべき抽象インターフェース。

#### メソッド

- `save(key: str, data: Any) -> bool` - データを保存
- `load(key: str) -> Optional[Any]` - データを読み込み
- `delete(key: str) -> bool` - データを削除
- `exists(key: str) -> bool` - データが存在するかチェック
- `clear() -> bool` - すべてのデータを削除

### MemoryDataRepository

メモリ内にデータを保存する実装。アプリケーション終了時にデータは失われます。

### FileDataRepository

JSON形式でファイルにデータを保存する実装。データは永続化されます。

#### コンストラクタ

```python
FileDataRepository(base_dir: str = "./data")
```

- `base_dir`: データファイルを保存するディレクトリ

### DataRepositoryFactory

データリポジトリを作成するファクトリクラス。

#### メソッド

```python
@staticmethod
def create(storage_type: str = "memory", **kwargs) -> IDataRepository
```

- `storage_type`: "memory" または "file"
- `**kwargs`: 各実装固有の引数（例: `base_dir`）

### Config

アプリケーション設定を管理するクラス。

#### プロパティ

- `storage_type: str` - ストレージタイプ（デフォルト: "memory"）
- `data_dir: str` - データディレクトリ（デフォルト: "./data"）

#### メソッド

- `get(key: str, default=None)` - 設定値を取得
- `set(key: str, value)` - 設定値を設定
- `save_to_file(config_file: str)` - 設定をファイルに保存

## トラブルシューティング

### ファイルが保存されない

- ディレクトリの書き込み権限を確認してください
- `base_dir` パラメータが正しいか確認してください
- エラーメッセージをコンソールで確認してください

### データが読み込めない

- ファイルが存在するか確認してください（`repo.exists(key)`）
- JSONファイルが壊れていないか確認してください
- ファイルのエンコーディングがUTF-8であることを確認してください

### メモリ使用量が多い

- ファイルベースストレージの使用を検討してください
- 不要なデータは定期的に削除してください（`repo.delete(key)` または `repo.clear()`）

## 将来の拡張

このシステムは、以下のような拡張が容易に可能です：

- **DatabaseDataRepository** - SQLiteやPostgreSQLなどのデータベースサポート
- **RedisDataRepository** - Redisキャッシュのサポート
- **CloudDataRepository** - AWS S3やGoogle Cloud Storageのサポート
- **EncryptedDataRepository** - 暗号化されたストレージ

新しい実装を追加するには、`IDataRepository`インターフェースを実装し、`DataRepositoryFactory`に登録するだけです。
