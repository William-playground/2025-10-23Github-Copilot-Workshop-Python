"""
データリポジトリのテスト

このファイルは、データリポジトリの実装が正しく動作することを確認します。
"""

import os
import shutil
from data_repository import (
    MemoryDataRepository,
    FileDataRepository,
    DataRepositoryFactory
)


def test_memory_repository():
    """メモリベースリポジトリのテスト"""
    print("テスト: MemoryDataRepository")
    
    repo = MemoryDataRepository()
    
    # 保存と読み込み
    assert repo.save("key1", {"data": "value1"}), "データ保存に失敗"
    assert repo.load("key1") == {"data": "value1"}, "データ読み込みに失敗"
    
    # 存在確認
    assert repo.exists("key1"), "存在するキーが見つからない"
    assert not repo.exists("key2"), "存在しないキーが見つかった"
    
    # 削除
    assert repo.delete("key1"), "データ削除に失敗"
    assert not repo.exists("key1"), "削除したキーがまだ存在する"
    assert repo.load("key1") is None, "削除したデータが読み込めた"
    
    # クリア
    repo.save("key1", "value1")
    repo.save("key2", "value2")
    assert repo.clear(), "クリアに失敗"
    assert not repo.exists("key1"), "クリア後にキーが存在する"
    assert not repo.exists("key2"), "クリア後にキーが存在する"
    
    print("  ✓ すべてのテストが成功")


def test_file_repository():
    """ファイルベースリポジトリのテスト"""
    print("テスト: FileDataRepository")
    
    test_dir = "./test_file_repo"
    
    try:
        repo = FileDataRepository(base_dir=test_dir)
        
        # 保存と読み込み
        assert repo.save("recipe1", {"name": "サンドイッチ", "score": 100}), "データ保存に失敗"
        data = repo.load("recipe1")
        assert data is not None, "データ読み込みに失敗"
        assert data["name"] == "サンドイッチ", "データが正しくない"
        assert data["score"] == 100, "データが正しくない"
        
        # ファイルが作成されたか確認
        expected_file = os.path.join(test_dir, "recipe1.json")
        assert os.path.exists(expected_file), "ファイルが作成されていない"
        
        # 存在確認
        assert repo.exists("recipe1"), "存在するキーが見つからない"
        assert not repo.exists("recipe2"), "存在しないキーが見つかった"
        
        # 削除
        assert repo.delete("recipe1"), "データ削除に失敗"
        assert not repo.exists("recipe1"), "削除したキーがまだ存在する"
        assert not os.path.exists(expected_file), "削除したファイルがまだ存在する"
        
        # クリア
        repo.save("key1", "value1")
        repo.save("key2", "value2")
        assert repo.clear(), "クリアに失敗"
        assert not repo.exists("key1"), "クリア後にキーが存在する"
        assert not repo.exists("key2"), "クリア後にキーが存在する"
        
        print("  ✓ すべてのテストが成功")
        
    finally:
        # クリーンアップ
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)


def test_factory():
    """ファクトリのテスト"""
    print("テスト: DataRepositoryFactory")
    
    # メモリベース
    memory_repo = DataRepositoryFactory.create("memory")
    assert isinstance(memory_repo, MemoryDataRepository), "メモリリポジトリが作成されない"
    
    # ファイルベース
    test_dir = "./test_factory_file"
    try:
        file_repo = DataRepositoryFactory.create("file", base_dir=test_dir)
        assert isinstance(file_repo, FileDataRepository), "ファイルリポジトリが作成されない"
        
        # 不正なタイプ
        try:
            DataRepositoryFactory.create("invalid")
            assert False, "不正なタイプでエラーが発生しない"
        except ValueError:
            pass  # 期待通りのエラー
        
        print("  ✓ すべてのテストが成功")
        
    finally:
        # クリーンアップ
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)


def test_path_traversal_protection():
    """パストラバーサル攻撃の防止テスト"""
    print("テスト: パストラバーサル攻撃の防止")
    
    test_dir = "./test_security"
    
    try:
        repo = FileDataRepository(base_dir=test_dir)
        
        # パストラバーサルを試みる
        repo.save("../../../etc/passwd", "malicious")
        
        # パストラバーサルが防がれていることを確認
        # basename が使用されるので "passwd.json" が test_dir 内に作成される
        expected_file = os.path.join(test_dir, "passwd.json")
        assert os.path.exists(expected_file), "セーフティ機構が動作していない"
        
        # システムファイルが上書きされていないことを確認
        assert not os.path.exists("/etc/passwd.json"), "パストラバーサルが成功してしまった"
        if os.path.exists("/etc/passwd"):
            # /etc/passwd が存在する場合（Linuxシステム）、それが変更されていないことを確認
            # 読み取り可能な場合のみチェック
            try:
                with open("/etc/passwd", "r") as f:
                    content = f.read()
                    assert "malicious" not in content, "システムファイルが改ざんされた"
            except PermissionError:
                pass  # 読み取り権限がない場合はスキップ
        
        print("  ✓ すべてのテストが成功")
        
    finally:
        # クリーンアップ
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)


def test_unicode_support():
    """Unicode文字のサポートテスト"""
    print("テスト: Unicode文字のサポート")
    
    test_dir = "./test_unicode"
    
    try:
        repo = FileDataRepository(base_dir=test_dir)
        
        # 日本語データ
        japanese_data = {
            "名前": "太郎",
            "趣味": ["読書", "料理", "旅行"],
            "メッセージ": "こんにちは、世界！"
        }
        
        assert repo.save("user_jp", japanese_data), "日本語データ保存に失敗"
        loaded_data = repo.load("user_jp")
        assert loaded_data is not None, "日本語データ読み込みに失敗"
        assert loaded_data["名前"] == "太郎", "日本語データが正しくない"
        assert loaded_data["メッセージ"] == "こんにちは、世界！", "日本語データが正しくない"
        
        print("  ✓ すべてのテストが成功")
        
    finally:
        # クリーンアップ
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)


def run_all_tests():
    """すべてのテストを実行"""
    print("=" * 60)
    print("データリポジトリのテスト実行")
    print("=" * 60)
    print()
    
    test_memory_repository()
    print()
    test_file_repository()
    print()
    test_factory()
    print()
    test_path_traversal_protection()
    print()
    test_unicode_support()
    print()
    
    print("=" * 60)
    print("すべてのテストが成功しました！")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()
