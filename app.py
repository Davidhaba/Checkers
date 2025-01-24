from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/<path:filename>')
def serve_file(filename):
    file_path = os.path.join('checkVerifications', filename)
    if os.path.exists(file_path):
        return send_from_directory('checkVerifications', filename)
    else:
        return "No found"

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
