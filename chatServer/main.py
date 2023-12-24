import socket
import json
import threading
import uuid


class Client:
    def __init__(self, username, color, client_socket):
        self.username = username
        self.color = color
        self.socket = client_socket


class Server:
    def __init__(self, port):
        self.clients = dict()
        self.clients_lock = threading.Lock()
        self.socket_lock = threading.Lock()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(("0.0.0.0", port))

    def start_server(self):
        self.server.listen()

        while True:
            conn, _ = self.server.accept()
            data = conn.recv(1024)
            print(data)
            message = json.loads(data.decode())

            client_uid = uuid.uuid4()
            self.clients[client_uid] = Client(message["username"], message["color"], conn)

            thread = threading.Thread(target=self.listen_client, args=(client_uid,), daemon=True)
            thread.start()

    def listen_client(self, client_uid):
        client_socket = self.clients[client_uid].socket

        while True:
            try:
                data = client_socket.recv(1024)
                message = json.loads(data.decode())
                print(message)
                if message["method"] == "message":
                    username, color = self.get_client_data(client_uid)
                    self.send_message({"username": username, "color": color,
                                       "message": message["message"]})
                elif message["method"] == "exit":
                    self.remove_client(client_uid)
                    return
            except:
                print(client_uid)
                self.remove_client(client_uid)
                return

    def get_client_data(self, client_uid):
        with self.clients_lock:
            return self.clients[client_uid].username, self.clients[client_uid].color

    def get_clients_connections(self):
        with self.clients_lock:
            return self.clients.keys()

    def remove_client(self, client_uid):
        with self.clients_lock:
            del self.clients[client_uid]

    def send_message(self, message):
        with self.socket_lock:
            for uid in self.get_clients_connections():
                self.clients[uid].socket.send(json.dumps(message).encode())


if __name__ == '__main__':
    server = Server(5555)
    server.start_server()
