from lib.message_passer import MessagePasser
import tkinter as tk
import random
import settings


class PrinterView(MessagePasser):
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.configure(bg=settings.OVERLAY_BACKGROUND_COLOR)

        self.sw = self.root.winfo_screenwidth()
        self.sh = self.root.winfo_screenheight()

        self.label = tk.Label(
            self.root,
            text="",
            font=settings.OVERLAY_FONT,
            fg=settings.OVERLAY_FONT_COLOR,
            bg=settings.OVERLAY_BACKGROUND_COLOR,
            padx=30,
            pady=20,
        )
        self.label.pack()

        self.root.withdraw()
        self.fade_in_ms = 200
        self.fade_out_ms = 500
        self.max_alpha = 0.85

    def show(self, text: str, display_duration_ms: int = 500):
        self.root.after(0, self._show_impl, text, display_duration_ms)

    def is_view_destroyed(self):
        try:
            return not self.root.winfo_exists()
        except tk.TclError:
            return True

    def destroy(self):
        if not self.is_view_destroyed():
            self.root.destroy()

    def _show_impl(self, text: str, display_duration_ms: int):
        self.label.config(text=text)

        self.root.update_idletasks()
        w = self.label.winfo_reqwidth()
        h = self.label.winfo_reqheight()
        x = (self.sw // 2) - (w // 2)
        y = int(self.sh * 0.75)

        self.root.geometry(f"{w}x{h}+{x}+{y}")
        self.root.deiconify()
        self.root.lift()

        self.fade_in(
            step=0.05,
            delay=20,
            final_callback=lambda: self.root.after(display_duration_ms, self.fade_out),
        )

    def fade_in(self, step=0.05, delay=20, final_callback=None):
        def _fade(alpha):
            if alpha < self.max_alpha:
                self.root.wm_attributes("-alpha", alpha)
                self.root.after(delay, _fade, alpha + step)
            else:
                self.root.wm_attributes("-alpha", self.max_alpha)
                if final_callback:
                    final_callback()

        _fade(0.0)

    def fade_out(self, step=0.05, delay=20):
        def _fade(alpha):
            if alpha > 0.0:
                self.root.wm_attributes("-alpha", alpha)
                self.root.after(delay, _fade, alpha - step)
            else:
                self.root.wm_attributes("-alpha", 0.0)
                self.root.withdraw()

        _fade(self.max_alpha)

    def run(self):
        self.root.mainloop()

    def receive(self, message: dict):
        print(f"printer view received, {message}")
