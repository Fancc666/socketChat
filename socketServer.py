from flask import Flask, request
from flask_socketio import SocketIO
from db import MyDatabase
import time

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return "<h1>Please Connect In WebSocket Method</h1>"

class Message:
    def __init__(self) -> None:
        self.status = {
            "online": {},# sid->name
            "history": []
        }
        self.limit = 2
    def generate_message(self, message_type):
        if message_type == "STATUS":
            return {
                "content": {
                    "online": [n for n in self.status["online"]],
                    "history": self.status["history"]
                }
            }
        if message_type == "JOIN":
            return {
                "content": request.sid
            }
        if message_type == "LEAVE":
            return {
                "content": request.sid
            }
        if message_type == "MESSAGE":
            return {
                "content": self.status["history"][-1],
                "sid": self.status["online"][request.sid]
            }
        if message_type == "NAME":
            return {
                "content": self.status["online"][request.sid]
            }
    def save_to_db(self, name, msg):
        # return
        db = MyDatabase("message.db")
        db.write_data("insert into message (time, name, msg) values (?, ?, ?)", (int(time.time()), name, msg))
        db.close()
    def send_message(self, msg_type, msg, to="all"):
        if to == "all":
            socketio.emit(msg_type, msg)
        if to == "only":
            socketio.emit(msg_type, msg, to=request.sid)
        if to == "ionly":
            socketio.emit(msg_type, msg, skip_sid=request.sid)
    def message_handler(self, msg):
        self.status["history"].append(msg)
        self.status["history"] = self.status["history"][self.limit*(-1):]
        self.send_message("MESSAGE", self.generate_message("MESSAGE"))
        self.save_to_db(self.status["online"][request.sid], msg)
    def connect_handler(self):
        self.status["online"][request.sid] = request.sid
        self.send_message("JOIN", self.generate_message("JOIN"), to="ionly")
        self.send_message("STATUS", self.generate_message("STATUS"), to="only")
    def disconnect_handler(self):
        self.send_message("LEAVE", self.generate_message("LEAVE"))
        del self.status["online"][request.sid]
    def name_handler(self, name):
        self.status["online"][request.sid] = name
        self.send_message("NAME", self.generate_message("NAME"))

message = Message()

@socketio.on('message')
def handle_message(msg):
    print('Received message: ', msg)
    message.message_handler(msg)
    # socketio.emit
@socketio.on('name')
def handele_name(msg):
    print('name change: ', msg, request.sid)
    message.name_handler(msg)

@socketio.on('connect')
def handle_connect():
    message.connect_handler()
    print("1 New Connect")

@socketio.on('disconnect')
def handle_disconnect():
    message.disconnect_handler()
    print("1 Connect Closed")

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5200, debug=True)
