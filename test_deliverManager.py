import unittest
from deliverManager import (
    KitchenObjectSO, RecipeSO, RecipeListSO,
    PlateKitchenObject, KitchenGameManager, DeliveryManager
)


class TestKitchenObjectSO(unittest.TestCase):
    """KitchenObjectSOのテストクラス"""
    
    def test_kitchen_object_creation(self):
        """キッチンオブジェクトの作成テスト"""
        obj = KitchenObjectSO("Tomato", 1)
        self.assertEqual(obj.name, "Tomato")
        self.assertEqual(obj.object_id, 1)


class TestPlateKitchenObject(unittest.TestCase):
    """PlateKitchenObjectのテストクラス"""
    
    def test_add_kitchen_object(self):
        """キッチンオブジェクトの追加テスト"""
        plate = PlateKitchenObject()
        tomato = KitchenObjectSO("Tomato", 1)
        plate.add_kitchen_object(tomato)
        objects = plate.get_kitchen_object_so_list()
        self.assertEqual(len(objects), 1)
        self.assertEqual(objects[0].name, "Tomato")
    
    def test_get_kitchen_object_so_list_returns_copy(self):
        """リストのコピーが返されることをテスト"""
        plate = PlateKitchenObject()
        tomato = KitchenObjectSO("Tomato", 1)
        plate.add_kitchen_object(tomato)
        
        objects1 = plate.get_kitchen_object_so_list()
        objects2 = plate.get_kitchen_object_so_list()
        
        # Different list objects but same content
        self.assertIsNot(objects1, objects2)
        self.assertEqual(len(objects1), len(objects2))


class TestKitchenGameManager(unittest.TestCase):
    """KitchenGameManagerのテストクラス"""
    
    def setUp(self):
        """各テスト前にシングルトンをリセット"""
        KitchenGameManager._instance = None
    
    def test_singleton_instance(self):
        """シングルトンパターンのテスト"""
        manager1 = KitchenGameManager.get_instance()
        manager2 = KitchenGameManager.get_instance()
        self.assertIs(manager1, manager2)
    
    def test_game_state(self):
        """ゲームの開始と停止のテスト"""
        manager = KitchenGameManager.get_instance()
        self.assertFalse(manager.is_game_playing())
        
        manager.start_game()
        self.assertTrue(manager.is_game_playing())
        
        manager.stop_game()
        self.assertFalse(manager.is_game_playing())


class TestDeliveryManager(unittest.TestCase):
    """DeliveryManagerのテストクラス"""
    
    def setUp(self):
        """各テスト前にシングルトンをリセット"""
        DeliveryManager._instance = None
        KitchenGameManager._instance = None
    
    def test_singleton_instance(self):
        """シングルトンパターンのテスト"""
        recipe_list = RecipeListSO([])
        manager1 = DeliveryManager.get_instance(recipe_list)
        manager2 = DeliveryManager.get_instance()
        self.assertIs(manager1, manager2)
    
    def test_deliver_matching_recipe(self):
        """一致するレシピの配達テスト"""
        # Setup
        tomato = KitchenObjectSO("Tomato", 1)
        lettuce = KitchenObjectSO("Lettuce", 2)
        salad_recipe = RecipeSO("Salad", [lettuce, tomato])
        recipe_list = RecipeListSO([salad_recipe])
        
        game_manager = KitchenGameManager.get_instance()
        game_manager.start_game()
        
        delivery_manager = DeliveryManager.get_instance(recipe_list)
        
        # Add recipe to waiting list manually
        delivery_manager._waiting_recipe_so_list.append(salad_recipe)
        
        # Create matching plate
        plate = PlateKitchenObject()
        plate.add_kitchen_object(lettuce)
        plate.add_kitchen_object(tomato)
        
        # Track events
        success_called = [False]
        
        def on_success(sender, args):
            success_called[0] = True
        
        delivery_manager.on_recipe_success.add_handler(on_success)
        
        # Deliver
        delivery_manager.deliver_recipe(plate)
        
        # Verify
        self.assertTrue(success_called[0])
        self.assertEqual(delivery_manager.get_successful_recipes_amount(), 1)
        self.assertEqual(len(delivery_manager.get_waiting_recipe_so_list()), 0)
    
    def test_deliver_non_matching_recipe(self):
        """一致しないレシピの配達テスト"""
        # Setup
        tomato = KitchenObjectSO("Tomato", 1)
        lettuce = KitchenObjectSO("Lettuce", 2)
        bread = KitchenObjectSO("Bread", 3)
        
        salad_recipe = RecipeSO("Salad", [lettuce, tomato])
        recipe_list = RecipeListSO([salad_recipe])
        
        game_manager = KitchenGameManager.get_instance()
        game_manager.start_game()
        
        delivery_manager = DeliveryManager.get_instance(recipe_list)
        
        # Add recipe to waiting list manually
        delivery_manager._waiting_recipe_so_list.append(salad_recipe)
        
        # Create non-matching plate (bread instead of expected ingredients)
        plate = PlateKitchenObject()
        plate.add_kitchen_object(bread)
        
        # Track events
        failed_called = [False]
        
        def on_failed(sender, args):
            failed_called[0] = True
        
        delivery_manager.on_recipe_failed.add_handler(on_failed)
        
        # Deliver
        delivery_manager.deliver_recipe(plate)
        
        # Verify
        self.assertTrue(failed_called[0])
        self.assertEqual(delivery_manager.get_successful_recipes_amount(), 0)
        self.assertEqual(len(delivery_manager.get_waiting_recipe_so_list()), 1)


if __name__ == '__main__':
    unittest.main()
