from flask import Flask, request, jsonify
from progress_manager import ProgressManager

app = Flask(__name__)

# 進捗マネージャーのインスタンスを取得
progress_manager = ProgressManager.get_instance()


@app.route('/api/progress', methods=['GET'])
def get_progress():
    """進捗データを取得するAPIエンドポイント"""
    try:
        result = progress_manager.get_progress()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/progress', methods=['POST'])
def save_progress():
    """進捗データを保存するAPIエンドポイント"""
    try:
        data = request.get_json()
        
        # 必須パラメータのチェック
        if not data:
            return jsonify({
                "success": False,
                "error": "リクエストボディが必要です"
            }), 400
        
        successful_recipes = data.get('successful_recipes', 0)
        total_deliveries = data.get('total_deliveries', 0)
        failed_deliveries = data.get('failed_deliveries', 0)
        
        result = progress_manager.save_progress(
            successful_recipes=successful_recipes,
            total_deliveries=total_deliveries,
            failed_deliveries=failed_deliveries
        )
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/progress/reset', methods=['POST'])
def reset_progress():
    """進捗データをリセットするAPIエンドポイント"""
    try:
        result = progress_manager.reset_progress()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/', methods=['GET'])
def index():
    """ルートエンドポイント"""
    return jsonify({
        "message": "進捗データ管理API",
        "endpoints": {
            "GET /api/progress": "進捗データを取得",
            "POST /api/progress": "進捗データを保存 (successful_recipes, total_deliveries, failed_deliveries)",
            "POST /api/progress/reset": "進捗データをリセット"
        }
    }), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
