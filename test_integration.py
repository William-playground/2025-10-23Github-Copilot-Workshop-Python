"""
統合テスト: DeliveryManagerとProgressManagerの連携をテスト
"""
from deliverManager import (
    KitchenObjectSO, RecipeSO, RecipeListSO, 
    PlateKitchenObject, DeliveryManager, KitchenGameManager
)
from progress_manager import ProgressManager

def test_integration():
    print("=== 統合テスト開始 ===\n")
    
    # 進捗データをリセット
    progress_manager = ProgressManager.get_instance()
    progress_manager.reset_progress()
    print("✓ 進捗データをリセット")
    
    # サンプルデータ作成
    tomato = KitchenObjectSO("Tomato", 1)
    lettuce = KitchenObjectSO("Lettuce", 2)
    bread = KitchenObjectSO("Bread", 3)
    
    # サンプルレシピ
    sandwich_recipe = RecipeSO("Sandwich", [bread, lettuce, tomato])
    salad_recipe = RecipeSO("Salad", [lettuce, tomato])
    
    recipe_list = RecipeListSO([sandwich_recipe, salad_recipe])
    
    # ゲームマネージャーとデリバリーマネージャーを初期化
    game_manager = KitchenGameManager.get_instance()
    game_manager.start_game()
    
    # DeliveryManagerの新しいインスタンスを作成するためにリセット
    DeliveryManager._instance = None
    delivery_manager = DeliveryManager.get_instance(recipe_list)
    
    print("✓ ゲームマネージャーとデリバリーマネージャーを初期化\n")
    
    # テスト1: 正しいレシピの配達（成功）
    print("テスト1: 正しいサンドイッチの配達")
    delivery_manager._waiting_recipe_so_list.append(sandwich_recipe)
    
    plate1 = PlateKitchenObject()
    plate1.add_kitchen_object(bread)
    plate1.add_kitchen_object(lettuce)
    plate1.add_kitchen_object(tomato)
    
    delivery_manager.deliver_recipe(plate1)
    
    progress = progress_manager.get_progress()
    print(f"  成功したレシピ数: {progress['data']['successful_recipes']}")
    print(f"  失敗した配達数: {progress['data']['failed_deliveries']}")
    print(f"  合計配達数: {progress['data']['total_deliveries']}")
    assert progress['data']['successful_recipes'] == 1
    assert progress['data']['failed_deliveries'] == 0
    assert progress['data']['total_deliveries'] == 1
    print("  ✓ 成功\n")
    
    # テスト2: 間違ったレシピの配達（失敗）
    print("テスト2: 間違った材料での配達")
    delivery_manager._waiting_recipe_so_list.append(salad_recipe)
    
    plate2 = PlateKitchenObject()
    plate2.add_kitchen_object(bread)  # サラダにパンは不要
    plate2.add_kitchen_object(lettuce)
    
    delivery_manager.deliver_recipe(plate2)
    
    progress = progress_manager.get_progress()
    print(f"  成功したレシピ数: {progress['data']['successful_recipes']}")
    print(f"  失敗した配達数: {progress['data']['failed_deliveries']}")
    print(f"  合計配達数: {progress['data']['total_deliveries']}")
    assert progress['data']['successful_recipes'] == 1
    assert progress['data']['failed_deliveries'] == 1
    assert progress['data']['total_deliveries'] == 2
    print("  ✓ 失敗が正しく記録された\n")
    
    # テスト3: 再度正しいレシピの配達
    print("テスト3: 正しいサラダの配達")
    delivery_manager._waiting_recipe_so_list.append(salad_recipe)
    
    plate3 = PlateKitchenObject()
    plate3.add_kitchen_object(lettuce)
    plate3.add_kitchen_object(tomato)
    
    delivery_manager.deliver_recipe(plate3)
    
    progress = progress_manager.get_progress()
    print(f"  成功したレシピ数: {progress['data']['successful_recipes']}")
    print(f"  失敗した配達数: {progress['data']['failed_deliveries']}")
    print(f"  合計配達数: {progress['data']['total_deliveries']}")
    assert progress['data']['successful_recipes'] == 2
    assert progress['data']['failed_deliveries'] == 1
    assert progress['data']['total_deliveries'] == 3
    print("  ✓ 成功\n")
    
    print("=== すべてのテストに合格しました！ ===")

if __name__ == "__main__":
    test_integration()
