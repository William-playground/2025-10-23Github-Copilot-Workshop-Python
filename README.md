# 2025 GitHub Copilot Workshop - Python

## 概要
このリポジトリは、GitHub Copilot ワークショップのためのPythonプロジェクトです。

ワークショップの手順：https://moulongzhang.github.io/2025-Github-Copilot-Workshop/github-copilot-workshop/#0

## プロジェクト構成

### コアファイル
- `deliverManager.py` - 配達管理システム（キッチンゲームのレシピ配達機能）
- `point.py` - 2D座標計算ユーティリティ
- `main.py` - メインエントリーポイント

### データ管理システム（第4段階実装）
- `data_repository.py` - データ管理の抽象化レイヤー
  - メモリベースとファイルベースのストレージをサポート
  - 将来的にはDB接続も追加可能な設計
- `config.py` - 設定管理システム
  - 環境変数または設定ファイルで切り替え可能
- `example_data_management.py` - 使用例
- `test_data_repository.py` - テストスイート
- `DATA_MANAGEMENT.md` - 詳細なドキュメント

## 使い方

### 基本的な実行
```bash
# 配達管理システムのデモ
python deliverManager.py

# データ管理システムの例
python example_data_management.py

# テスト実行
python test_data_repository.py
```

### データストレージの切り替え

#### 環境変数を使用
```bash
# ファイルストレージを使用
export STORAGE_TYPE=file
export DATA_DIR=./game_data
python deliverManager.py

# メモリストレージを使用
export STORAGE_TYPE=memory
python deliverManager.py
```

#### 設定ファイルを使用
```python
from config import get_config

config = get_config()
config.set("storage_type", "file")
config.set("data_dir", "./my_data")
config.save_to_file("./app_config.json")
```

詳細は [DATA_MANAGEMENT.md](DATA_MANAGEMENT.md) を参照してください。

## 機能

### データ管理の抽象化（第4段階）
- ✅ 抽象インターフェース（IDataRepository）
- ✅ メモリベース実装（MemoryDataRepository）
- ✅ ファイルベース実装（FileDataRepository）
- ✅ 設定による切り替え機能
- ✅ 自動状態保存機能
- ✅ セキュリティ保護（パストラバーサル対策）
- ✅ Unicode/日本語対応

## 開発

### テスト
すべてのテストを実行：
```bash
python test_data_repository.py
```

### セキュリティ
このプロジェクトには以下のセキュリティ対策が実装されています：
- パストラバーサル攻撃の防止
- ファイルパスのサニタイゼーション
- 安全なファイル操作

## ライセンス
ワークショップ用プロジェクト
