import time
import threading
import sys
import signal
import argparse
from bindake import Bindake
from bindake.keyboard import MyKeyboard
from bindake.makefile_config import MakefileConfig
from bindake.printer_view import PrinterView
from bindake.settings import Settings

stop_event = threading.Event()

g_bindake = None
g_view = None


def handle_exit(_signum, _frame):
    if g_bindake:
        g_bindake.destroy()


def check_stop_event():
    if stop_event.is_set():
        handle_exit(None, None)
        return

    # Check again in 100ms
    if g_view:
        g_view.root.after(100, check_stop_event)


def read_args():
    settings = Settings()
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        default=False,
        help="Enable verbose output",
    )
    parser.add_argument(
        "-s",
        "--boot-wait",
        type=int,
        default=30,
        help="Wait N seconds before booting (default: 0)",
    )
    args: argparse.Namespace = parser.parse_args()

    settings.verbose = args.verbose
    settings.boot_wait = args.boot_wait

    return settings


def main():
    # args:
    # - -v verbose mode
    # - overlay=disabled

    settings = read_args()

    if settings.boot_wait > 0:
        time.sleep(settings.boot_wait)

    global g_bindake
    global g_view
    my_keyboard = MyKeyboard(notify_to=[], stop_event=stop_event)
    view = PrinterView()
    bindake = Bindake(
        my_keyboard=my_keyboard, view=view, stop_event=stop_event, settings=settings
    )
    g_bindake = bindake
    g_view = view

    makefile = MakefileConfig(filepath="/home/martin/.config/bindake/Makefile")
    makefile.parse()
    bindake.makefile = makefile

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
