from lib.message_passer import MessagePasser
import tkinter as tk
import random


class PrinterView(MessagePasser):
    def __init__(self):
        self.root = tk.Tk()

        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.wm_attributes("-alpha", 0.1)  # Whole window semi-transparent
        self.root.configure(bg="black")

        self.label = tk.Label(
            self.root,
            text="",
            font=("Courier New", 36, "bold"),
            bg="black",
            fg="lime",
        )
        self.label.pack()

        self.sw, self.sh = (
            self.root.winfo_screenwidth(),
            self.root.winfo_screenheight(),
        )

        self.root.withdraw()

    def show(self, message, duration=2000):
        self.label.config(text=message)
        self.label.update_idletasks()

        w = self.label.winfo_width()
        h = self.label.winfo_height()
        x = self.sw // 2 - w // 2
        y = int(self.sh * 0.90 - h // 2)
        self.root.geometry(f"{w}x{h}+{x}+{y}")

        self.root.deiconify()
        self.root.after(duration, self.root.withdraw)

    def run(self):
        self.root.mainloop()

    def receive(self, message: dict):
        print(f"printer view received, {message}")
