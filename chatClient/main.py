import threading

from gui import Interface
from messages import Messages


def receive_messages(interface, messages):
    while True:
        if interface.client is None:
            continue
        message = interface.client.receive_message()
        messages.add_message(message)


if __name__ == "__main__":
    messages = Messages()
    interface = Interface(messages)
    threading.Thread(target=receive_messages,args=(interface, messages), daemon=True).start()
    interface.start()
