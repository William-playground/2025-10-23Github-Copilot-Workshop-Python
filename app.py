from flask import Flask, jsonify, request
from point import Point2D
from deliverManager import (
    KitchenObjectSO, RecipeSO, RecipeListSO, 
    PlateKitchenObject, DeliveryManager, KitchenGameManager
)

app = Flask(__name__)

# Initialize sample data
tomato = KitchenObjectSO("Tomato", 1)
lettuce = KitchenObjectSO("Lettuce", 2)
bread = KitchenObjectSO("Bread", 3)

sandwich_recipe = RecipeSO("Sandwich", [bread, lettuce, tomato])
salad_recipe = RecipeSO("Salad", [lettuce, tomato])
recipe_list = RecipeListSO([sandwich_recipe, salad_recipe])


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "ok"}), 200


@app.route('/api/recipes', methods=['GET'])
def get_recipes():
    """Get all available recipes"""
    recipes = []
    for recipe in recipe_list.recipe_so_list:
        recipes.append({
            "name": recipe.name,
            "ingredients": [
                {"name": obj.name, "id": obj.object_id} 
                for obj in recipe.kitchen_object_so_list
            ]
        })
    return jsonify({"recipes": recipes}), 200


@app.route('/api/point/distance', methods=['POST'])
def calculate_distance():
    """Calculate distance between two points"""
    data = request.get_json()
    
    if not data or 'point1' not in data or 'point2' not in data:
        return jsonify({"error": "Invalid request data"}), 400
    
    try:
        p1 = Point2D(data['point1']['x'], data['point1']['y'])
        p2 = Point2D(data['point2']['x'], data['point2']['y'])
        distance = p1.distance_to(p2)
        
        return jsonify({
            "distance": distance,
            "point1": {"x": p1.x, "y": p1.y},
            "point2": {"x": p2.x, "y": p2.y}
        }), 200
    except (KeyError, TypeError, ValueError) as e:
        return jsonify({"error": f"Invalid point data: {str(e)}"}), 400


@app.route('/api/game/start', methods=['POST'])
def start_game():
    """Start the game"""
    game_manager = KitchenGameManager.get_instance()
    game_manager.start_game()
    return jsonify({"status": "game_started", "is_playing": game_manager.is_game_playing()}), 200


@app.route('/api/game/stop', methods=['POST'])
def stop_game():
    """Stop the game"""
    game_manager = KitchenGameManager.get_instance()
    game_manager.stop_game()
    return jsonify({"status": "game_stopped", "is_playing": game_manager.is_game_playing()}), 200


@app.route('/api/game/status', methods=['GET'])
def game_status():
    """Get game status"""
    game_manager = KitchenGameManager.get_instance()
    return jsonify({"is_playing": game_manager.is_game_playing()}), 200


if __name__ == '__main__':
    app.run(debug=True, port=5000)
