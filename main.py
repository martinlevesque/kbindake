from dataclasses import dataclass
from pynput import keyboard
import tkinter as tk
import random
from typing import Union
import subprocess
from bindake import Bindake


def show_notification(message):
    root = tk.Tk()
    root.overrideredirect(True)
    root.attributes("-topmost", True)
    root.configure(bg='black')

    # Get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Create label with tech-style font
    label = tk.Label(
        root,
        text=message,
        font=("Courier New", 36, "bold"),
        bg="black",
        fg="lime"
    )
    label.pack()

    # Center horizontally, position near bottom (e.g., 90% of screen height)
    label.update_idletasks()
    width = label.winfo_width()
    height = label.winfo_height()
    x = (screen_width // 2) - (width // 2)
    x += random.randint(1, 100)
    y = int(screen_height * 0.90) - (height // 2)
    y -= random.randint(1, 100)

    root.geometry(f"{width}x{height}+{x}+{y}")

    # Auto-close after 2 seconds
    root.after(2000, root.destroy)
    root.mainloop()

# Keep track of which keys are pressed
current_keys = set()

def on_press(key):
    current_keys.add(key)

    print(key)
    command_name = "firefox"

    # Check if Ctrl + Alt + C are all pressed
    if (
        keyboard.Key.ctrl_l in current_keys or keyboard.Key.ctrl_r in current_keys
    ) and (
        keyboard.Key.alt_l in current_keys or keyboard.Key.alt_r in current_keys
    ) and (
        key == keyboard.KeyCode.from_char('f')
    ):
        result = subprocess.run(["make", command_name], timeout=10, capture_output=True, text=True)
        print(result.stdout)
        print(result.stderr)
        print(result.returncode)

        if result.returncode == 0:
            result.stdout.split("\n")
            output_to_show = result.stdout.splitlines()[-1]
            show_notification(output_to_show)
        else:
            show_notification(f"Error with {command_name}, {result.stdout}, {result.stderr}")

def on_release(key: Union[keyboard.Key, keyboard.KeyCode, None]):
    current_keys.discard(key)

def main():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        bindake = Bindake(listener = listener)
        bindake.listen()

if __name__ == "__main__":
    main()


