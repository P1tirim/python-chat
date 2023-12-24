import tkinter
from tkinter import Tk, ttk, NW, colorchooser, SOLID
from tkinter.messagebox import showerror
from tkinter.scrolledtext import ScrolledText

from client import Client


class Interface:
    def __init__(self, messages):
        self.client = None
        self.messages = messages
        self.root = Tk()
        self.root.title("Chat")

        self.root.geometry("200x110")

        ttk.Label(text="Введите имя и выберите цвет:").pack(anchor=NW, padx=5, pady=5)
        entry_name = ttk.Entry()
        entry_name.pack(anchor=NW, padx=5, pady=5)

        self.color = "#000000"

        def select_color():
            self.color = colorchooser.askcolor(initialcolor="black")[1]
            button_color["bg"] = self.color

        button_color = tkinter.Button(bg="black", command=select_color)
        button_color.place(x=140, y=35, width=20, height=20)

        def chat_connect():
            if entry_name.get() == "":
                return

            try:
                self.client = Client(entry_name.get(), self.color)
                self.chat_window()
                self.root.after(100, self.receive_messages)
            except:
                showerror(title="Ошибка", message="Ошибка подключения к серверу")

        tkinter.Button(text="Продолжить", command=chat_connect).pack(anchor=NW, padx=5, pady=5)

    def chat_window(self):
        self.root.destroy()
        self.root = Tk()
        self.root.title = "chat"
        self.root.geometry("600x725")

        frame = ttk.Frame(borderwidth=1, relief=SOLID, padding=[8, 10], width=550, height=600)
        canvas = tkinter.Canvas(frame, width=550, height=600)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor=NW)
        canvas.configure(yscrollcommand=scrollbar.set)

        frame.pack(anchor=NW, padx=5, pady=5)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        text_message = ScrolledText(width=100, height=2, wrap="word")
        text_message.pack(anchor=NW, padx=5, pady=5, expand=True)

        def send_message():
            if text_message.get("1.0", "end-1c") == "":
                return
            self.client.send_message({"method": "message", "message": text_message.get("1.0", "end-1c")})
            text_message.delete("1.0", "end-1c")

        ttk.Button(text="Отправить", command=send_message).pack(anchor=NW, padx=5)

    def receive_messages(self):
        messages = self.messages.get_messages()
        for message in messages:
            print(message)
            frame_label = ttk.Frame(self.scrollable_frame, width=600, height=10)
            ttk.Label(frame_label, text=message["username"] + ":", foreground=message["color"], justify="left").pack(side="left")
            ttk.Label(frame_label, text=message["message"], wraplength=500, justify="left").pack(side="left")
            frame_label.pack(anchor=NW, fill="x", expand=True)

        self.root.after(100, self.receive_messages)

    def start(self):
        self.root.mainloop()

