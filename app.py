from flask import Flask, request
from flask_socketio import SocketIO, emit, join_room, leave_room
import eventlet

eventlet.monkey_patch()

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Route to confirm backend is live
@app.route("/")
def index():
    return "WebRTC Signaling Server is running."

# Handle client connection to a session
@socketio.on('join')
def handle_join(data):
    token = data.get('token')
    join_room(token)
    emit('joined', {'message': f'Joined session {token}'}, room=request.sid)
    print(f"[JOIN] {request.sid} joined {token}")

# Relay WebRTC messages (offer/answer/ice) to others in the session
@socketio.on('signal')
def handle_signal(data):
    token = data.get('token')
    message = data.get('message')
    emit('signal', message, room=token, include_self=False)
    print(f"[SIGNAL] {request.sid} relayed {message['type']} to {token}")

# Optional: Handle client disconnect
@socketio.on('disconnect')
def handle_disconnect():
    print(f"[DISCONNECT] {request.sid} disconnected.")

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8080)
