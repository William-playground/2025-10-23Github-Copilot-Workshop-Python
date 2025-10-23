import json
import os
from datetime import datetime
from typing import Optional, Dict, Any
from dataclasses import dataclass, field, asdict


@dataclass
class ProgressData:
    """進捗データクラス"""
    successful_recipes: int = 0
    total_deliveries: int = 0
    failed_deliveries: int = 0
    last_updated: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        """辞書形式に変換"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ProgressData':
        """辞書から生成"""
        return cls(**data)


class ProgressManager:
    """進捗データ管理クラス（Singleton）"""
    
    _instance: Optional['ProgressManager'] = None
    _data_file_path = "progress_data.json"
    
    def __init__(self):
        self._progress_data = ProgressData()
        self._load_from_file()
    
    @classmethod
    def get_instance(cls) -> 'ProgressManager':
        """Singletonインスタンスを取得"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def _load_from_file(self):
        """ファイルから進捗データを読み込む"""
        if os.path.exists(self._data_file_path):
            try:
                with open(self._data_file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._progress_data = ProgressData.from_dict(data)
            except (json.JSONDecodeError, IOError) as e:
                print(f"進捗データの読み込みエラー: {e}")
                self._progress_data = ProgressData()
    
    def _save_to_file(self):
        """ファイルに進捗データを保存"""
        try:
            with open(self._data_file_path, 'w', encoding='utf-8') as f:
                json.dump(self._progress_data.to_dict(), f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"進捗データの保存エラー: {e}")
    
    def save_progress(self, successful_recipes: int, total_deliveries: int, failed_deliveries: int) -> Dict[str, Any]:
        """進捗データを保存"""
        self._progress_data.successful_recipes = successful_recipes
        self._progress_data.total_deliveries = total_deliveries
        self._progress_data.failed_deliveries = failed_deliveries
        self._progress_data.last_updated = datetime.now().isoformat()
        
        self._save_to_file()
        
        return {
            "success": True,
            "message": "進捗データを保存しました",
            "data": self._progress_data.to_dict()
        }
    
    def get_progress(self) -> Dict[str, Any]:
        """進捗データを取得"""
        return {
            "success": True,
            "data": self._progress_data.to_dict()
        }
    
    def update_successful_recipes(self, count: int = 1):
        """成功したレシピ数を更新"""
        self._progress_data.successful_recipes += count
        self._progress_data.total_deliveries += count
        self._progress_data.last_updated = datetime.now().isoformat()
        self._save_to_file()
    
    def update_failed_deliveries(self, count: int = 1):
        """失敗した配達数を更新"""
        self._progress_data.failed_deliveries += count
        self._progress_data.total_deliveries += count
        self._progress_data.last_updated = datetime.now().isoformat()
        self._save_to_file()
    
    def reset_progress(self) -> Dict[str, Any]:
        """進捗データをリセット"""
        self._progress_data = ProgressData()
        self._save_to_file()
        
        return {
            "success": True,
            "message": "進捗データをリセットしました",
            "data": self._progress_data.to_dict()
        }


# 使用例
if __name__ == "__main__":
    # 進捗マネージャーのインスタンスを取得
    progress_manager = ProgressManager.get_instance()
    
    # 進捗データを保存
    result = progress_manager.save_progress(
        successful_recipes=10,
        total_deliveries=15,
        failed_deliveries=5
    )
    print("保存結果:", result)
    
    # 進捗データを取得
    result = progress_manager.get_progress()
    print("取得結果:", result)
    
    # 成功したレシピ数を更新
    progress_manager.update_successful_recipes()
    print("更新後:", progress_manager.get_progress())
