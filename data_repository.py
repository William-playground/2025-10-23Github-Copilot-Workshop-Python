"""
データ管理の抽象化インターフェースと実装

このモジュールはメモリベースとファイルベースのデータストレージを
抽象化し、切り替え可能にします。
"""

from abc import ABC, abstractmethod
from typing import Any, Optional, Dict
import json
import os
from pathlib import Path


class IDataRepository(ABC):
    """データリポジトリの抽象インターフェース"""
    
    @abstractmethod
    def save(self, key: str, data: Any) -> bool:
        """データを保存する
        
        Args:
            key: データのキー
            data: 保存するデータ
            
        Returns:
            成功した場合True、失敗した場合False
        """
        pass
    
    @abstractmethod
    def load(self, key: str) -> Optional[Any]:
        """データを読み込む
        
        Args:
            key: データのキー
            
        Returns:
            データが存在する場合はデータ、存在しない場合はNone
        """
        pass
    
    @abstractmethod
    def delete(self, key: str) -> bool:
        """データを削除する
        
        Args:
            key: データのキー
            
        Returns:
            成功した場合True、失敗した場合False
        """
        pass
    
    @abstractmethod
    def exists(self, key: str) -> bool:
        """データが存在するかチェックする
        
        Args:
            key: データのキー
            
        Returns:
            存在する場合True、存在しない場合False
        """
        pass
    
    @abstractmethod
    def clear(self) -> bool:
        """すべてのデータを削除する
        
        Returns:
            成功した場合True、失敗した場合False
        """
        pass


class MemoryDataRepository(IDataRepository):
    """メモリベースのデータリポジトリ実装"""
    
    def __init__(self):
        """メモリベースのデータリポジトリを初期化"""
        self._storage: Dict[str, Any] = {}
    
    def save(self, key: str, data: Any) -> bool:
        """データをメモリに保存する"""
        try:
            self._storage[key] = data
            return True
        except Exception as e:
            print(f"メモリへの保存エラー: {e}")
            return False
    
    def load(self, key: str) -> Optional[Any]:
        """メモリからデータを読み込む"""
        return self._storage.get(key)
    
    def delete(self, key: str) -> bool:
        """メモリからデータを削除する"""
        try:
            if key in self._storage:
                del self._storage[key]
                return True
            return False
        except Exception as e:
            print(f"メモリからの削除エラー: {e}")
            return False
    
    def exists(self, key: str) -> bool:
        """メモリにデータが存在するかチェック"""
        return key in self._storage
    
    def clear(self) -> bool:
        """メモリからすべてのデータを削除"""
        try:
            self._storage.clear()
            return True
        except Exception as e:
            print(f"メモリクリアエラー: {e}")
            return False


class FileDataRepository(IDataRepository):
    """ファイルベースのデータリポジトリ実装（JSON形式）"""
    
    def __init__(self, base_dir: str = "./data"):
        """ファイルベースのデータリポジトリを初期化
        
        Args:
            base_dir: データファイルを保存するベースディレクトリ
        """
        self._base_dir = Path(base_dir)
        self._base_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_file_path(self, key: str) -> Path:
        """キーからファイルパスを生成"""
        # セキュリティ: パストラバーサルを防ぐ
        safe_key = key.replace("/", "_").replace("\\", "_")
        return self._base_dir / f"{safe_key}.json"
    
    def save(self, key: str, data: Any) -> bool:
        """データをファイルに保存する"""
        try:
            file_path = self._get_file_path(key)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"ファイル保存エラー: {e}")
            return False
    
    def load(self, key: str) -> Optional[Any]:
        """ファイルからデータを読み込む"""
        try:
            file_path = self._get_file_path(key)
            if not file_path.exists():
                return None
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"ファイル読み込みエラー: {e}")
            return None
    
    def delete(self, key: str) -> bool:
        """ファイルを削除する"""
        try:
            file_path = self._get_file_path(key)
            if file_path.exists():
                file_path.unlink()
                return True
            return False
        except Exception as e:
            print(f"ファイル削除エラー: {e}")
            return False
    
    def exists(self, key: str) -> bool:
        """ファイルが存在するかチェック"""
        file_path = self._get_file_path(key)
        return file_path.exists()
    
    def clear(self) -> bool:
        """すべてのデータファイルを削除"""
        try:
            for file_path in self._base_dir.glob("*.json"):
                file_path.unlink()
            return True
        except Exception as e:
            print(f"ファイルクリアエラー: {e}")
            return False


class DataRepositoryFactory:
    """データリポジトリのファクトリクラス"""
    
    @staticmethod
    def create(storage_type: str = "memory", **kwargs) -> IDataRepository:
        """データリポジトリを作成する
        
        Args:
            storage_type: ストレージタイプ ("memory" または "file")
            **kwargs: 各実装固有の引数
            
        Returns:
            データリポジトリインスタンス
            
        Raises:
            ValueError: 未知のストレージタイプの場合
        """
        if storage_type.lower() == "memory":
            return MemoryDataRepository()
        elif storage_type.lower() == "file":
            base_dir = kwargs.get("base_dir", "./data")
            return FileDataRepository(base_dir=base_dir)
        else:
            raise ValueError(f"未知のストレージタイプ: {storage_type}")


# 使用例
if __name__ == "__main__":
    print("=== メモリベースのリポジトリテスト ===")
    memory_repo = DataRepositoryFactory.create("memory")
    
    # データ保存
    memory_repo.save("user1", {"name": "太郎", "score": 100})
    memory_repo.save("user2", {"name": "花子", "score": 200})
    
    # データ読み込み
    print(f"user1: {memory_repo.load('user1')}")
    print(f"user2: {memory_repo.load('user2')}")
    print(f"user3 存在: {memory_repo.exists('user3')}")
    
    # データ削除
    memory_repo.delete("user1")
    print(f"user1削除後: {memory_repo.load('user1')}")
    
    print("\n=== ファイルベースのリポジトリテスト ===")
    file_repo = DataRepositoryFactory.create("file", base_dir="./test_data")
    
    # データ保存
    file_repo.save("recipe1", {"name": "サンドイッチ", "ingredients": ["パン", "レタス", "トマト"]})
    file_repo.save("recipe2", {"name": "サラダ", "ingredients": ["レタス", "トマト"]})
    
    # データ読み込み
    print(f"recipe1: {file_repo.load('recipe1')}")
    print(f"recipe2: {file_repo.load('recipe2')}")
    
    # ファイル存在確認
    print(f"recipe1 存在: {file_repo.exists('recipe1')}")
    
    # クリーンアップ
    file_repo.clear()
    import shutil
    if os.path.exists("./test_data"):
        shutil.rmtree("./test_data")
    
    print("\n完了!")
