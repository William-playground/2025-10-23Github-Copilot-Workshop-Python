"""
アプリケーション設定管理

環境変数または設定ファイルからアプリケーションの設定を読み込みます。
"""

import os
import json
from pathlib import Path
from typing import Optional


class Config:
    """アプリケーション設定クラス"""
    
    # デフォルト値
    DEFAULT_STORAGE_TYPE = "memory"
    DEFAULT_DATA_DIR = "./data"
    
    def __init__(self, config_file: Optional[str] = None):
        """設定を初期化
        
        Args:
            config_file: 設定ファイルのパス（オプション）
        """
        self._config_data = {}
        
        # 設定ファイルから読み込み
        if config_file and os.path.exists(config_file):
            self._load_from_file(config_file)
        
        # 環境変数で上書き（優先度が高い）
        self._load_from_env()
    
    def _load_from_file(self, config_file: str):
        """設定ファイルから読み込む"""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                self._config_data = json.load(f)
        except Exception as e:
            print(f"設定ファイル読み込みエラー: {e}")
    
    def _load_from_env(self):
        """環境変数から読み込む"""
        # STORAGE_TYPE環境変数
        storage_type = os.getenv("STORAGE_TYPE")
        if storage_type:
            self._config_data["storage_type"] = storage_type
        
        # DATA_DIR環境変数
        data_dir = os.getenv("DATA_DIR")
        if data_dir:
            self._config_data["data_dir"] = data_dir
    
    @property
    def storage_type(self) -> str:
        """ストレージタイプを取得"""
        return self._config_data.get("storage_type", self.DEFAULT_STORAGE_TYPE)
    
    @property
    def data_dir(self) -> str:
        """データディレクトリを取得"""
        return self._config_data.get("data_dir", self.DEFAULT_DATA_DIR)
    
    def get(self, key: str, default=None):
        """設定値を取得
        
        Args:
            key: 設定キー
            default: デフォルト値
            
        Returns:
            設定値
        """
        return self._config_data.get(key, default)
    
    def set(self, key: str, value):
        """設定値を設定
        
        Args:
            key: 設定キー
            value: 設定値
        """
        self._config_data[key] = value
    
    def save_to_file(self, config_file: str):
        """設定をファイルに保存
        
        Args:
            config_file: 設定ファイルのパス
        """
        try:
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(self._config_data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"設定ファイル保存エラー: {e}")
            return False


# グローバル設定インスタンス
_global_config: Optional[Config] = None


def get_config(config_file: Optional[str] = None) -> Config:
    """グローバル設定インスタンスを取得
    
    Args:
        config_file: 設定ファイルのパス（初回のみ有効）
        
    Returns:
        設定インスタンス
    """
    global _global_config
    if _global_config is None:
        _global_config = Config(config_file)
    return _global_config


def reset_config():
    """グローバル設定をリセット（テスト用）"""
    global _global_config
    _global_config = None


# 使用例
if __name__ == "__main__":
    print("=== 設定管理のテスト ===")
    
    # デフォルト設定
    config = get_config()
    print(f"ストレージタイプ: {config.storage_type}")
    print(f"データディレクトリ: {config.data_dir}")
    
    # 設定を変更
    config.set("storage_type", "file")
    config.set("data_dir", "./my_data")
    print(f"\n変更後のストレージタイプ: {config.storage_type}")
    print(f"変更後のデータディレクトリ: {config.data_dir}")
    
    # ファイルに保存
    config.save_to_file("./test_config.json")
    print("\n設定ファイルを保存しました: test_config.json")
    
    # 新しい設定インスタンスで読み込み
    reset_config()
    config2 = get_config("./test_config.json")
    print(f"\nファイルから読み込んだストレージタイプ: {config2.storage_type}")
    print(f"ファイルから読み込んだデータディレクトリ: {config2.data_dir}")
    
    # クリーンアップ
    if os.path.exists("./test_config.json"):
        os.remove("./test_config.json")
    
    print("\n完了!")
