# CI/CD セットアップガイド

## 概要
このプロジェクトにGitHub Actionsを使用したCI/CDパイプラインを実装しました。

## 実装内容

### 1. テストファイルの作成

#### test_point.py
`point.py`モジュールの`Point2D`クラスをテストします。
- 基本的な距離計算
- 同一点の距離（ゼロ）
- 負の座標の処理
- 文字列表現

#### test_deliverManager.py
`deliverManager.py`モジュールのゲーム管理機能をテストします。
- `KitchenObjectSO`の作成
- `PlateKitchenObject`の機能
- `KitchenGameManager`のシングルトンパターンとゲーム状態
- `DeliveryManager`のレシピマッチングと配達ロジック

### 2. GitHub Actionsワークフロー

ファイル: `.github/workflows/python-tests.yml`

#### トリガー条件
- `main`または`master`ブランチへのプッシュ
- `main`または`master`ブランチへのプルリクエスト

#### テスト環境
- Ubuntu最新版
- Python 3.10, 3.11, 3.12（マトリックスビルド）

#### 実行ステップ
1. コードのチェックアウト
2. 指定バージョンのPythonセットアップ
3. Pythonバージョンの表示
4. `test_point.py`の実行
5. `test_deliverManager.py`の実行
6. すべてのテストの一括実行

## ローカルでのテスト実行

### 個別のテストファイルを実行
```bash
python -m unittest test_point.py -v
python -m unittest test_deliverManager.py -v
```

### すべてのテストを実行
```bash
python -m unittest discover -s . -p "test_*.py" -v
```

## GitHub上での確認方法

1. GitHubリポジトリページにアクセス
2. 「Actions」タブをクリック
3. 「Python Tests」ワークフローを選択
4. 各実行結果をクリックして詳細を確認

## テスト結果

すべてのテストが正常に動作することを確認済み：
- test_point.py: 4つのテスト
- test_deliverManager.py: 8つのテスト
- 合計: 12のテストケース

## 完了条件の確認

✅ GitHub Actionsのワークフローファイルを作成
✅ プッシュ時に自動テストが実行される
✅ テスト結果がGitHub上で確認できる
