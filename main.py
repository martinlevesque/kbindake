import time
import threading
import sys
import signal
from bindake import Bindake
from bindake.keyboard import MyKeyboard
from bindake.makefile_config import MakefileConfig
from bindake.printer_view import PrinterView

stop_event = threading.Event()

my_keyboard = MyKeyboard(notify_to=[], stop_event=stop_event)
view = PrinterView()
bindake = Bindake(my_keyboard=my_keyboard, view=view, stop_event=stop_event)


def handle_exit(_signum, _frame):
    bindake.destroy()


def check_stop_event():
    if stop_event.is_set():
        handle_exit(None, None)
        return

    # Check again in 100ms
    view.root.after(100, check_stop_event)


def main():
    # args:
    # - -v verbose mode
    # - overlay=disabled

    mc = MakefileConfig(filepath="./Makefile.sample")
    print(mc.read_file_lines())

    # Register signal handlers
    signal.signal(signal.SIGINT, handle_exit)  # Ctrl+C
    signal.signal(signal.SIGTERM, handle_exit)  # kill <pid>

    # Start periodic checking
    view.root.after(100, check_stop_event)

    my_keyboard.notify_to = [bindake]

    thread = threading.Thread(target=bindake.loop, daemon=True)
    thread.start()

    try:
        view.run()  # blocks
    except KeyboardInterrupt:
        handle_exit(signal.SIGINT, None)


if __name__ == "__main__":
    main()
