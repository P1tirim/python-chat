import socket
import json
import threading


class Client:
    def __init__(self, username, color):
        self.socket_lock = threading.Lock()
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(("localhost", 5555))
        self.send_message({"username": username, "color": color})

    def send_message(self, message):
        with self.socket_lock:
            self.client.send(json.dumps(message).encode())

    def receive_message(self):
        data = self.client.recv(1024)
        return json.loads(data.decode())

    def close_client(self):
        self.client.close()
