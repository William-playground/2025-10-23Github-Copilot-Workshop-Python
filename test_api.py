"""
APIエンドポイントのテストスクリプト
"""
import requests
import json

BASE_URL = "http://localhost:5000"

def test_api():
    print("=== APIエンドポイントテスト ===\n")
    
    # テスト1: ルートエンドポイント
    print("テスト1: GET / (ルートエンドポイント)")
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200
    data = response.json()
    print(f"  ステータス: {response.status_code}")
    print(f"  メッセージ: {data['message']}")
    print("  ✓ 成功\n")
    
    # テスト2: 進捗データをリセット
    print("テスト2: POST /api/progress/reset (リセット)")
    response = requests.post(f"{BASE_URL}/api/progress/reset")
    assert response.status_code == 200
    data = response.json()
    assert data['success'] == True
    assert data['data']['successful_recipes'] == 0
    assert data['data']['total_deliveries'] == 0
    assert data['data']['failed_deliveries'] == 0
    print(f"  ステータス: {response.status_code}")
    print(f"  メッセージ: {data['message']}")
    print(f"  データ: {data['data']}")
    print("  ✓ 成功\n")
    
    # テスト3: 進捗データを取得
    print("テスト3: GET /api/progress (取得)")
    response = requests.get(f"{BASE_URL}/api/progress")
    assert response.status_code == 200
    data = response.json()
    assert data['success'] == True
    assert data['data']['successful_recipes'] == 0
    print(f"  ステータス: {response.status_code}")
    print(f"  データ: {data['data']}")
    print("  ✓ 成功\n")
    
    # テスト4: 進捗データを保存
    print("テスト4: POST /api/progress (保存)")
    test_data = {
        "successful_recipes": 5,
        "total_deliveries": 7,
        "failed_deliveries": 2
    }
    response = requests.post(
        f"{BASE_URL}/api/progress",
        json=test_data,
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data['success'] == True
    assert data['data']['successful_recipes'] == 5
    assert data['data']['total_deliveries'] == 7
    assert data['data']['failed_deliveries'] == 2
    print(f"  ステータス: {response.status_code}")
    print(f"  メッセージ: {data['message']}")
    print(f"  保存データ: {data['data']}")
    print("  ✓ 成功\n")
    
    # テスト5: 保存されたデータを再度取得して確認
    print("テスト5: GET /api/progress (保存後の確認)")
    response = requests.get(f"{BASE_URL}/api/progress")
    assert response.status_code == 200
    data = response.json()
    assert data['success'] == True
    assert data['data']['successful_recipes'] == 5
    assert data['data']['total_deliveries'] == 7
    assert data['data']['failed_deliveries'] == 2
    print(f"  ステータス: {response.status_code}")
    print(f"  データ: {data['data']}")
    print("  ✓ 保存されたデータが正しく取得できた\n")
    
    # テスト6: 部分的なデータ更新
    print("テスト6: POST /api/progress (部分更新)")
    partial_data = {
        "successful_recipes": 10,
        "total_deliveries": 12,
        "failed_deliveries": 2
    }
    response = requests.post(
        f"{BASE_URL}/api/progress",
        json=partial_data,
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data['data']['successful_recipes'] == 10
    print(f"  ステータス: {response.status_code}")
    print(f"  更新データ: {data['data']}")
    print("  ✓ 成功\n")
    
    print("=== すべてのAPIテストに合格しました！ ===")

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("エラー: APIサーバーが起動していません。")
        print("先に `python3 main.py` でサーバーを起動してください。")
    except AssertionError as e:
        print(f"テスト失敗: {e}")
    except Exception as e:
        print(f"予期しないエラー: {e}")
