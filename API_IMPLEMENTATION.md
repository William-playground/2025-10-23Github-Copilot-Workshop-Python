# API Communication Implementation

This document describes the implementation of the API communication layer for the Pomodoro Timer application (Stage 4: API連携・データ永続化).

## Overview

The API communication layer separates frontend-backend communication into dedicated modules, following best practices for code organization and maintainability.

## Architecture

```
┌─────────────────┐
│  Frontend (JS)  │
│  ┌───────────┐  │
│  │ timer.js  │  │  ← Timer logic and UI control
│  └─────┬─────┘  │
│        │        │
│  ┌─────▼─────┐  │
│  │  api.js   │  │  ← API communication layer
│  └─────┬─────┘  │
└────────┼────────┘
         │ HTTP
         │ (JSON)
┌────────▼────────┐
│  Backend (Flask)│
│  ┌───────────┐  │
│  │  app.py   │  │  ← API endpoints
│  └───────────┘  │
│                 │
│  In-memory      │
│  data store     │
└─────────────────┘
```

## File Structure

```
.
├── app.py                    # Flask backend with API endpoints
├── templates/
│   └── index.html           # Main UI template
├── static/
│   └── js/
│       ├── api.js           # API communication module
│       └── timer.js         # Timer logic with API integration
└── requirements.txt         # Python dependencies
```

## API Endpoints

### 1. GET /api/progress
Retrieves current progress data.

**Response:**
```json
{
  "completed_count": 0,
  "total_focus_time": 0,
  "last_updated": "2025-10-23T07:52:31.614263"
}
```

### 2. POST /api/progress
Saves progress data when timer completes.

**Request:**
```json
{
  "completed_count": 1,
  "total_focus_time": 25
}
```

**Response:**
```json
{
  "success": true,
  "message": "Progress saved successfully",
  "data": {
    "completed_count": 1,
    "total_focus_time": 25,
    "last_updated": "2025-10-23T07:52:03.407166"
  }
}
```

### 3. POST /api/progress/reset
Resets progress data to zero.

**Response:**
```json
{
  "success": true,
  "message": "Progress reset successfully",
  "data": {
    "completed_count": 0,
    "total_focus_time": 0,
    "last_updated": "2025-10-23T07:52:31.614263"
  }
}
```

## JavaScript API Module (static/js/api.js)

The `API` object provides three main functions:

### saveProgress(progressData)
Saves progress data to the server.

```javascript
await API.saveProgress({
  completed_count: 1,
  total_focus_time: 25
});
```

### getProgress()
Retrieves current progress from the server.

```javascript
const data = await API.getProgress();
console.log(data.completed_count, data.total_focus_time);
```

### resetProgress()
Resets progress on the server.

```javascript
await API.resetProgress();
```

All functions:
- Use modern `async/await` syntax
- Return Promises for easy error handling
- Include comprehensive error logging
- Handle HTTP errors appropriately

## Timer Integration

The `PomodoroTimer` class in `timer.js` integrates with the API:

1. **On Page Load**: Calls `API.getProgress()` to load existing progress
2. **On Timer Completion**: Calls `API.saveProgress()` to save updated progress
3. **Error Handling**: Displays user-friendly alerts on API failures

### Timer Completion Flow

```
Timer reaches 0:00
    ↓
Update local state
    ↓
Update UI display
    ↓
API.saveProgress() ← Sends data to server
    ↓
Success confirmation
```

## Installation & Running

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run the Application
```bash
python app.py
```

The application will start on `http://localhost:5000`

## Testing

### Manual API Testing

Test GET endpoint:
```bash
curl http://localhost:5000/api/progress
```

Test POST endpoint:
```bash
curl -X POST http://localhost:5000/api/progress \
  -H "Content-Type: application/json" \
  -d '{"completed_count": 1, "total_focus_time": 25}'
```

Test RESET endpoint:
```bash
curl -X POST http://localhost:5000/api/progress/reset
```

### Browser Console Testing

Open browser console and test:
```javascript
// Get progress
await API.getProgress();

// Save progress
await API.saveProgress({
  completed_count: 3,
  total_focus_time: 75
});

// Reset progress
await API.resetProgress();
```

## Features Implemented

✅ **Separation of Concerns**: API logic separated into dedicated module
✅ **Async/Await**: Modern JavaScript async patterns
✅ **Error Handling**: Comprehensive error handling and logging
✅ **RESTful Design**: Clean, RESTful API endpoints
✅ **Automatic Integration**: Timer automatically calls API on completion
✅ **Progress Persistence**: Data survives page refreshes (in-memory)
✅ **User Feedback**: Console logging and error alerts

## Future Enhancements

- Add database persistence (currently using in-memory storage)
- Implement user authentication
- Add data visualization (charts, graphs)
- Export progress data
- Multiple timer configurations
- Sound notifications on completion

## Completion Criteria (Stage 4)

All requirements met:
- ✅ API communication functions created in static/js/
- ✅ Timer completion triggers API call
- ✅ Progress data correctly sent to server

## Dependencies

- **Flask 3.0.0**: Web framework for Python
- Modern browser with ES6+ support (for async/await)
