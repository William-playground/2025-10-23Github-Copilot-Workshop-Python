from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

# Simple in-memory storage for progress data (can be replaced with database later)
progress_data = {
    'completed_count': 0,
    'total_focus_time': 0,  # in minutes
    'last_updated': None
}

@app.route('/')
def index():
    """Serve the main pomodoro timer page"""
    return render_template('index.html')

@app.route('/api/progress', methods=['GET'])
def get_progress():
    """Get current progress data"""
    return jsonify(progress_data)

@app.route('/api/progress', methods=['POST'])
def save_progress():
    """Save progress data when timer completes"""
    try:
        data = request.get_json()
        
        # Update progress data
        if 'completed_count' in data:
            progress_data['completed_count'] = data['completed_count']
        
        if 'total_focus_time' in data:
            progress_data['total_focus_time'] = data['total_focus_time']
        
        progress_data['last_updated'] = datetime.now().isoformat()
        
        return jsonify({
            'success': True,
            'message': 'Progress saved successfully',
            'data': progress_data
        }), 200
    
    except Exception as e:
        # Log error for debugging but don't expose details to client
        app.logger.error(f'Error saving progress: {str(e)}')
        return jsonify({
            'success': False,
            'message': 'Error saving progress. Please try again.'
        }), 400

@app.route('/api/progress/reset', methods=['POST'])
def reset_progress():
    """Reset progress data"""
    progress_data['completed_count'] = 0
    progress_data['total_focus_time'] = 0
    progress_data['last_updated'] = datetime.now().isoformat()
    
    return jsonify({
        'success': True,
        'message': 'Progress reset successfully',
        'data': progress_data
    })

if __name__ == '__main__':
    import os
    # Only enable debug mode in development
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
