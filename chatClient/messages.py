import threading


class Messages:
    def __init__(self):
        self.messages = []
        self.lock = threading.Lock()

    def add_message(self, message):
        with self.lock:
            self.messages.append(message)

    def get_messages(self):
        with self.lock:
            messages = self.messages
            self.messages = []
            return messages
