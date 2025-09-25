import socketio

# Connect to your server
sio = socketio.Client()

@sio.on('connect')
def on_connect():
    print('Connected!')

@sio.on('past_24_hours') 
def on_past_data(data):
    print(f"Got {data['count']} past activities:")
    for activity in data['activities']:
        print(f"  - {activity['description']}")

@sio.on('new_activity')
def on_new_activity(data):
    print("🔥 New activity received:")
    print(f"🔥 NEW: {data}")

sio.connect('http://localhost:5003')
sio.wait()