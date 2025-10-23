"""
データ管理抽象化の使用例

このファイルは、メモリベースとファイルベースのデータストレージを
切り替えて使用する例を示します。
"""

import time
from deliverManager import (
    KitchenObjectSO, RecipeSO, RecipeListSO,
    PlateKitchenObject, KitchenGameManager, DeliveryManager
)
from data_repository import DataRepositoryFactory
from config import get_config, reset_config


def example_with_memory_storage():
    """メモリベースストレージの例"""
    print("=" * 60)
    print("メモリベースストレージの例")
    print("=" * 60)
    
    # サンプルデータ作成
    tomato = KitchenObjectSO("Tomato", 1)
    lettuce = KitchenObjectSO("Lettuce", 2)
    bread = KitchenObjectSO("Bread", 3)
    
    # サンプルレシピ
    sandwich_recipe = RecipeSO("Sandwich", [bread, lettuce, tomato])
    salad_recipe = RecipeSO("Salad", [lettuce, tomato])
    
    recipe_list = RecipeListSO([sandwich_recipe, salad_recipe])
    
    # メモリベースのデータリポジトリを作成
    memory_repo = DataRepositoryFactory.create("memory")
    
    # ゲームマネージャーとデリバリーマネージャーを初期化
    game_manager = KitchenGameManager.get_instance()
    game_manager.start_game()
    
    # デリバリーマネージャーをリセット（前のインスタンスをクリア）
    DeliveryManager._instance = None
    delivery_manager = DeliveryManager.get_instance(recipe_list, memory_repo)
    
    # イベントハンドラー追加
    def on_success(sender, args):
        print("✓ レシピ配達成功！")
    
    def on_failed(sender, args):
        print("✗ レシピ配達失敗...")
    
    delivery_manager.on_recipe_success.add_handler(on_success)
    delivery_manager.on_recipe_failed.add_handler(on_failed)
    
    print("ゲーム開始...")
    
    # レシピをスポーン（待機リストに追加）
    delivery_manager._waiting_recipe_so_list.append(sandwich_recipe)
    print(f"待機中のレシピ: {[r.name for r in delivery_manager.get_waiting_recipe_so_list()]}")
    
    # レシピを配達
    plate = PlateKitchenObject()
    plate.add_kitchen_object(bread)
    plate.add_kitchen_object(lettuce)
    plate.add_kitchen_object(tomato)
    
    print("サンドイッチを配達...")
    delivery_manager.deliver_recipe(plate)
    
    print(f"成功したレシピ数: {delivery_manager.get_successful_recipes_amount()}")
    
    # メモリに保存されたデータを確認
    state = memory_repo.load("delivery_manager_state")
    print(f"メモリに保存された状態: {state}")
    
    game_manager.stop_game()
    print("\n")


def example_with_file_storage():
    """ファイルベースストレージの例"""
    print("=" * 60)
    print("ファイルベースストレージの例")
    print("=" * 60)
    
    # サンプルデータ作成
    tomato = KitchenObjectSO("Tomato", 1)
    lettuce = KitchenObjectSO("Lettuce", 2)
    bread = KitchenObjectSO("Bread", 3)
    cheese = KitchenObjectSO("Cheese", 4)
    
    # サンプルレシピ
    sandwich_recipe = RecipeSO("Sandwich", [bread, lettuce, tomato])
    cheese_sandwich = RecipeSO("Cheese Sandwich", [bread, cheese])
    
    recipe_list = RecipeListSO([sandwich_recipe, cheese_sandwich])
    
    # ファイルベースのデータリポジトリを作成
    file_repo = DataRepositoryFactory.create("file", base_dir="./game_data")
    
    # ゲームマネージャーとデリバリーマネージャーを初期化
    game_manager = KitchenGameManager.get_instance()
    game_manager.start_game()
    
    # デリバリーマネージャーをリセット（前のインスタンスをクリア）
    DeliveryManager._instance = None
    delivery_manager = DeliveryManager.get_instance(recipe_list, file_repo)
    
    print("ゲーム開始...")
    
    # レシピをスポーン（待機リストに追加）
    delivery_manager._waiting_recipe_so_list.append(sandwich_recipe)
    delivery_manager._waiting_recipe_so_list.append(cheese_sandwich)
    print(f"待機中のレシピ: {[r.name for r in delivery_manager.get_waiting_recipe_so_list()]}")
    
    # レシピを配達
    plate1 = PlateKitchenObject()
    plate1.add_kitchen_object(bread)
    plate1.add_kitchen_object(lettuce)
    plate1.add_kitchen_object(tomato)
    
    print("サンドイッチを配達...")
    delivery_manager.deliver_recipe(plate1)
    
    plate2 = PlateKitchenObject()
    plate2.add_kitchen_object(bread)
    plate2.add_kitchen_object(cheese)
    
    print("チーズサンドイッチを配達...")
    delivery_manager.deliver_recipe(plate2)
    
    print(f"成功したレシピ数: {delivery_manager.get_successful_recipes_amount()}")
    
    # ファイルに保存されたデータを確認
    state = file_repo.load("delivery_manager_state")
    print(f"ファイルに保存された状態: {state}")
    print(f"データはディレクトリ './game_data' に保存されています")
    
    game_manager.stop_game()
    print("\n")


def example_with_config_file():
    """設定ファイルを使用した例"""
    print("=" * 60)
    print("設定ファイルを使用した例")
    print("=" * 60)
    
    # 設定ファイルを作成
    reset_config()
    config = get_config()
    config.set("storage_type", "file")
    config.set("data_dir", "./persistent_data")
    config.save_to_file("./app_config.json")
    
    print("設定ファイル 'app_config.json' を作成しました")
    print(f"  ストレージタイプ: {config.storage_type}")
    print(f"  データディレクトリ: {config.data_dir}")
    
    # サンプルデータ作成
    tomato = KitchenObjectSO("Tomato", 1)
    lettuce = KitchenObjectSO("Lettuce", 2)
    bread = KitchenObjectSO("Bread", 3)
    
    # サンプルレシピ
    sandwich_recipe = RecipeSO("Sandwich", [bread, lettuce, tomato])
    recipe_list = RecipeListSO([sandwich_recipe])
    
    # 設定ファイルから自動的にデータリポジトリが作成される
    reset_config()
    config = get_config("./app_config.json")
    
    game_manager = KitchenGameManager.get_instance()
    game_manager.start_game()
    
    # デリバリーマネージャーをリセット（前のインスタンスをクリア）
    DeliveryManager._instance = None
    delivery_manager = DeliveryManager.get_instance(recipe_list)  # data_repositoryを指定しない
    
    print("\nゲーム開始（設定ファイルから読み込み）...")
    
    # レシピをスポーン（待機リストに追加）
    delivery_manager._waiting_recipe_so_list.append(sandwich_recipe)
    print(f"待機中のレシピ: {[r.name for r in delivery_manager.get_waiting_recipe_so_list()]}")
    
    # レシピを配達
    plate = PlateKitchenObject()
    plate.add_kitchen_object(bread)
    plate.add_kitchen_object(lettuce)
    plate.add_kitchen_object(tomato)
    
    print("サンドイッチを配達...")
    delivery_manager.deliver_recipe(plate)
    
    print(f"成功したレシピ数: {delivery_manager.get_successful_recipes_amount()}")
    print(f"データはディレクトリ '{config.data_dir}' に保存されています")
    
    game_manager.stop_game()
    print("\n")


if __name__ == "__main__":
    # 各例を実行
    example_with_memory_storage()
    example_with_file_storage()
    example_with_config_file()
    
    print("=" * 60)
    print("すべての例が完了しました！")
    print("=" * 60)
    print("\n作成されたファイルとディレクトリ:")
    print("  - ./game_data/")
    print("  - ./persistent_data/")
    print("  - ./app_config.json")
    print("\nこれらは手動で削除できます。")
