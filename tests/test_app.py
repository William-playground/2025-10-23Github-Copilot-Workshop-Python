import pytest
import sys
import os

# Add parent directory to path to import app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app


@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_health_check(client):
    """Test the health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'ok'


def test_get_recipes(client):
    """Test getting all recipes"""
    response = client.get('/api/recipes')
    assert response.status_code == 200
    data = response.get_json()
    assert 'recipes' in data
    assert len(data['recipes']) > 0
    
    # Check recipe structure
    recipe = data['recipes'][0]
    assert 'name' in recipe
    assert 'ingredients' in recipe


def test_calculate_distance_valid(client):
    """Test distance calculation with valid points"""
    payload = {
        'point1': {'x': 0, 'y': 0},
        'point2': {'x': 3, 'y': 4}
    }
    response = client.post('/api/point/distance', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert 'distance' in data
    assert data['distance'] == 5.0  # 3-4-5 triangle


def test_calculate_distance_invalid_data(client):
    """Test distance calculation with invalid data"""
    payload = {
        'point1': {'x': 0, 'y': 0}
        # Missing point2
    }
    response = client.post('/api/point/distance', json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data


def test_calculate_distance_no_data(client):
    """Test distance calculation with no data"""
    response = client.post('/api/point/distance', json={})
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data


def test_start_game(client):
    """Test starting the game"""
    response = client.post('/api/game/start')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'game_started'
    assert data['is_playing'] is True


def test_stop_game(client):
    """Test stopping the game"""
    # Start the game first
    client.post('/api/game/start')
    
    # Stop the game
    response = client.post('/api/game/stop')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'game_stopped'
    assert data['is_playing'] is False


def test_game_status(client):
    """Test getting game status"""
    response = client.get('/api/game/status')
    assert response.status_code == 200
    data = response.get_json()
    assert 'is_playing' in data
    assert isinstance(data['is_playing'], bool)


def test_game_workflow(client):
    """Test complete game workflow"""
    # Check initial status
    response = client.get('/api/game/status')
    initial_status = response.get_json()
    
    # Start game
    response = client.post('/api/game/start')
    assert response.status_code == 200
    assert response.get_json()['is_playing'] is True
    
    # Check status after start
    response = client.get('/api/game/status')
    assert response.get_json()['is_playing'] is True
    
    # Stop game
    response = client.post('/api/game/stop')
    assert response.status_code == 200
    assert response.get_json()['is_playing'] is False
    
    # Check status after stop
    response = client.get('/api/game/status')
    assert response.get_json()['is_playing'] is False
