from flask import Flask
from flask_socketio import SocketIO, emit
from threading import Thread
import subprocess
import math

from utils.vision_subscriber import VisionSubscriber
from utils.converter import todict
import rclpy

app = Flask(__name__)
socketio = SocketIO(app,  cors_allowed_origins="*")
global vision_running

@socketio.on("connect")
def handle_connect():
    print("Client connected")
    global thread
    global stop_thread
    stop_thread = False
    if thread is None:
        thread = Thread(target=vision_callback)
        thread.start()

@socketio.on("disconnect")
def handle_disconnect():
    print("Client disconnected")
    global thread
    global stop_thread
    stop_thread = True
    thread = None

@socketio.on("fieldSide")
def handle_field_side(side):
    #TODO get side to rest of the code
    if side == True:
        print("Field is on the left side", flush=True)
    elif side == False:
        print("Field is on the right side", flush=True)

@socketio.on("teamColor")
def handle_team_color(color):
    #TODO get color to rest of the code
    if color == True:
        print("Team color is blue", flush=True)
    elif color == False:
        print("Team color is yellow", flush=True)

def handle_output(pipe, callback):
    """
    Read output from a pipe and pass it to a callback line by line.
    """
    with pipe:
        for line in iter(pipe.readline, b''):
            callback(line.decode())

def print_output(line):
    """
    Handle a single line of output.
    """
    global vision_running
    socketio.emit("visionOutput", {"line": line})
    socketio.emit("visionStatus", {"status": vision_running})
    print(f'linha{line}', end='')

@socketio.on("refereeButton")
def handle_referee_button():
    pass

@socketio.on("visionButton")
def handle_vision_button():
    global vision_running, process
    command = ['ros2', 'run', 'demo_nodes_py', 'talker']
    if vision_running:
        vision_running = False
        socketio.emit("visionStatus", {"status": vision_running})
        socketio.emit("visionOutput", {"line": "Terminating vision node"})
        subprocess.run(['killall']+[command[-1]])

    else:
        vision_running = True
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Create and start threads to handle stdout and stderr
        stdout_thread = Thread(target=handle_output, args=(process.stdout, print_output))
        stderr_thread = Thread(target=handle_output, args=(process.stderr, print_output))
        stdout_thread.start()
        stderr_thread.start()

@socketio.on("communicationButton")
def handle_communication_button():
    pass

@socketio.on("message")
def handle_message(message):
    print(f"Received message: {message}", flush=True)

def vision_callback():
    rclpy.init()
    vision_subs = VisionSubscriber()
    while True:
        rclpy.spin_once(vision_subs)
        data = vision_subs.get_data()
        data = todict(data)
        socketio.emit("vision_msg", {"data": data})


def main():
    global thread, vision_running
    thread = None
    vision_running = False
    socketio.run(app, debug=True, use_reloader=False, log_output=False)

if __name__ == "__main__":
    main()