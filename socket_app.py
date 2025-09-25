from flask import Flask, jsonify, request
from flask_socketio import SocketIO, emit
from datetime import datetime, timedelta
import threading
import time
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
socketio = SocketIO(app, cors_allowed_origins="*")

# Simple list to store activities (like a database table)
activities = []

def add_activity(activity_type, user_id, description):
    """Add a new activity and notify all connected clients"""
    
    # Create the activity
    activity = {
        'id': len(activities) + 1,
        'type': activity_type,
        'user_id': user_id, 
        'description': description,
        'timestamp': datetime.now().isoformat(),
        'created_at': datetime.now()  # For filtering
    }
    
    # Add to our "database"
    activities.append(activity)
    print(f"📝 New activity: {description}")
    
    # Send to all connected WebSocket clients in real-time
    # Remove created_at before sending (it's not JSON serializable)
    clean_activity = {
        'id': activity['id'],
        'type': activity['type'],
        'user_id': activity['user_id'],
        'description': activity['description'],
        'timestamp': activity['timestamp']
    }
    socketio.emit('new_activity', clean_activity)
    
    return activity

def get_last_24_hours():
    """Get all activities from the past 24 hours"""
    cutoff_time = datetime.now() - timedelta(hours=24)
    
    recent_activities = []
    for activity in activities:
        if activity['created_at'] > cutoff_time:
            # Remove the created_at field (only used internally)
            clean_activity = {
                'id': activity['id'],
                'type': activity['type'],
                'user_id': activity['user_id'],
                'description': activity['description'],
                'timestamp': activity['timestamp']
            }
            recent_activities.append(clean_activity)
    
    # Sort by newest first
    return sorted(recent_activities, key=lambda x: x['timestamp'], reverse=True)

# REST API ROUTES

@app.route('/api/activities/recent', methods=['GET'])
def get_recent_activities():
    """REST API: Get activities from past 24 hours"""
    recent = get_last_24_hours()
    
    return jsonify({
        'success': True,
        'count': len(recent),
        'activities': recent
    })

@app.route('/api/activities', methods=['POST'])
def create_activity():
    """REST API: Create a new activity"""
    data = request.get_json()
    
    # Validate required fields
    if not data or not all(field in data for field in ['type', 'user_id', 'description']):
        return jsonify({
            'success': False,
            'error': 'Need: type, user_id, description'
        }), 400
    
    # Create the activity
    activity = add_activity(
        activity_type=data['type'],
        user_id=data['user_id'], 
        description=data['description']
    )
    
    return jsonify({
        'success': True,
        'activity': {
            'id': activity['id'],
            'type': activity['type'],
            'user_id': activity['user_id'],
            'description': activity['description'],
            'timestamp': activity['timestamp']
        }
    }), 201

# WEBSOCKET EVENTS

@socketio.on('connect')
def handle_connect():
    """When client connects, send them past 24 hours of data"""
    print(f"🔌 Client connected")
    
    # Get past 24 hours of activities
    recent_activities = get_last_24_hours()
    
    # Send them all the historical data
    emit('past_24_hours', {
        'activities': recent_activities,
        'count': len(recent_activities),
        'message': f'Here are {len(recent_activities)} activities from past 24 hours'
    })

@socketio.on('disconnect')
def handle_disconnect():
    """When client disconnects"""
    print(f"❌ Client disconnected")

# DEMO: Create some sample data
def create_sample_data():
    """Create some activities from the past 24 hours for testing"""
    sample_activities = [
        ('user_login', 'john_doe', 'John logged into the system'),
        ('file_upload', 'jane_smith', 'Jane uploaded report.pdf'),
        ('task_complete', 'bob_wilson', 'Bob completed the review task'),
        ('user_logout', 'alice_brown', 'Alice logged out'),
        ('comment_added', 'john_doe', 'John commented on issue #123')
    ]
    
    # Create activities with random times in past 24 hours
    for i, (act_type, user, desc) in enumerate(sample_activities):
        # Create activity at different times in the past
        hours_ago = random.uniform(1, 23)  # 1-23 hours ago
        past_time = datetime.now() - timedelta(hours=hours_ago)
        
        activity = {
            'id': i + 1,
            'type': act_type,
            'user_id': user,
            'description': desc,
            'timestamp': past_time.isoformat(),
            'created_at': past_time
        }
        activities.append(activity)
    
    print(f"📚 Created {len(sample_activities)} sample activities")

# DEMO: Simulate new activities every 10 seconds
def simulate_new_activities():
    """Background task: Create new activities every 10 seconds"""
    counter = len(activities) + 1
    
    while True:
        time.sleep(10)  # Wait 10 seconds
        
        # Create a random new activity
        users = ['john_doe', 'jane_smith', 'bob_wilson', 'alice_brown']
        actions = [
            ('user_login', 'logged in'),
            ('file_upload', 'uploaded a file'), 
            ('task_complete', 'completed a task'),
            ('comment_added', 'added a comment')
        ]
        
        user = random.choice(users)
        action_type, action_desc = random.choice(actions)
        
        add_activity(
            activity_type=action_type,
            user_id=user,
            description=f"{user} {action_desc}"
        )
        counter += 1

if __name__ == '__main__':
    print("🚀 Starting Activity Feed API...")
    
    # Create some sample historical data
    create_sample_data()
    
    # Start background thread to simulate new activities
    bg_thread = threading.Thread(target=simulate_new_activities, daemon=True)
    bg_thread.start()
    
    print("📡 Server running on http://localhost:5000")
    print("🔗 REST API: GET /api/activities/recent")
    print("🔗 REST API: POST /api/activities") 
    print("⚡ WebSocket: Connects automatically send past 24hr data")
    print("⚡ WebSocket: New activities pushed in real-time")
    
    socketio.run(app, debug=True, host='0.0.0.0', port=5003)