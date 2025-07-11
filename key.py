from pynput import keyboard
import tkinter as tk


#import subprocess
#def show_notification(message):
#    subprocess.run(['notify-send', message])


def show_notification(message):
    root = tk.Tk()
    root.overrideredirect(True)  # No window decorations
    root.attributes("-topmost", True)  # Always on top
    root.configure(bg='black')

    # Get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Create label with tech-style font
    label = tk.Label(
        root,
        text=message,
        font=("Courier New", 36, "bold"),  # Tech-style font
        bg="black",
        fg="lime"  # Matrix-style color
    )
    label.pack()

    # Center horizontally, position near bottom (e.g., 90% of screen height)
    label.update_idletasks()
    width = label.winfo_width()
    height = label.winfo_height()
    x = (screen_width // 2) - (width // 2)
    y = int(screen_height * 0.90) - (height // 2)

    root.geometry(f"{width}x{height}+{x}+{y}")

    # Auto-close after 2 seconds
    root.after(2000, root.destroy)
    root.mainloop()

# Keep track of which keys are pressed
current_keys = set()

def on_press(key):
    current_keys.add(key)

    # Check if Ctrl + Alt + C are all pressed
    if (
        keyboard.Key.ctrl_l in current_keys or keyboard.Key.ctrl_r in current_keys
    ) and (
        keyboard.Key.alt_l in current_keys or keyboard.Key.alt_r in current_keys
    ) and (
        key == keyboard.KeyCode.from_char('c')
    ):
        show_notification("ctrl + alt + c was pressed!")
        print("Ctrl + Alt + C was pressed!")

def on_release(key):
    # Remove the key when released
    current_keys.discard(key)

    # Optionally stop on ESC
    if key == keyboard.Key.esc:
        return False

# Start listener
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

