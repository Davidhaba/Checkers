from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, leave_room, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

rooms = {}

@app.route('/')
def index():
    return render_template('main.html')

@socketio.on('join_game')
def handle_join(data):
    room = data['room']
    join_room(room)
    if room not in rooms:
        rooms[room] = {'players': 0, 'state': None}
    rooms[room]['players'] += 1
    emit('player_joined', {'players': rooms[room]['players']}, room=room)

@socketio.on('leave_game')
def handle_leave(data):
    room = data['room']
    leave_room(room)
    if room in rooms:
        rooms[room]['players'] -= 1
        if rooms[room]['players'] == 0:
            del rooms[room]

@socketio.on('move')
def handle_move(data):
    room = data['room']
    rooms[room]['state'] = data['state']
    emit('update_board', data, room=room)

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
