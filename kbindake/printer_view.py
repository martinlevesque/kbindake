import tkinter as tk
from screeninfo import get_monitors, Monitor
from tkinter import font as tkfont
from lib.message_passer import MessagePasser
import settings
from kbindake import logger


class PrinterView(MessagePasser):
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.configure(bg=settings.OVERLAY_BACKGROUND_COLOR)

        self.monitor = None
        self.update_screen()

        # Store base font info for dynamic sizing
        self.base_font_family = (
            settings.OVERLAY_FONT[0]
            if isinstance(settings.OVERLAY_FONT, tuple)
            else "Arial"
        )

        self.build_label()
        self.root.withdraw()
        self.max_alpha = 0.85

    def build_label(self):
        self.label = tk.Label(
            self.root,
            text="",
            font=settings.OVERLAY_FONT,
            fg=settings.OVERLAY_FONT_COLOR,
            bg=settings.OVERLAY_BACKGROUND_COLOR,
            padx=30,
            pady=20,
            justify="left",
            wraplength=self.max_width - 60,
        )
        self.label.pack()

        return self.label

    def update_screen(self):
        self.monitor = self.get_active_monitor()

        screen_height = None
        screen_width = None

        if self.monitor:
            screen_width = self.monitor.width
            screen_height = self.monitor.height
        else:
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()

        if screen_width:
            self.max_width = int(screen_width * 0.9)

        if screen_height:
            self.max_height = int(screen_height * 0.9)

    def get_mouse_position(self):
        x = self.root.winfo_pointerx()
        y = self.root.winfo_pointery()

        return x, y

    def get_active_monitor(self) -> Monitor | None:
        mouse_x, mouse_y = self.get_mouse_position()

        for m in get_monitors():
            if m.x <= mouse_x < m.x + m.width and m.y <= mouse_y < m.y + m.height:
                return m

        return None

    def calculate_optimal_font_size(self, text: str):
        """Calculate optimal font size based on text length and screen size"""
        nb_lines = len(text.split("\n"))

        # Calculate new font size
        new_size = settings.overlay_font_size(nb_lines)

        return new_size

    def show(self, text: str, display_duration_ms: int = 500):
        if hasattr(self, "hide_timer") and self.hide_timer:
            self.root.after_cancel(self.hide_timer)
            self.hide_timer = None

        self.update_screen()

        nb_lines = len(str(text).split("\n"))
        self.display_text_for(text, display_duration_ms * nb_lines)

    def is_view_destroyed(self):
        try:
            return not self.root.winfo_exists()
        except tk.TclError:
            return True

    def destroy(self):
        if not self.is_view_destroyed():
            self.root.destroy()

    def display_text_for(self, text: str, display_duration_ms: int):
        if not self.monitor:
            logger.error("No monitor available.")
            return

        # Calculate optimal font size for this text
        optimal_font_size = self.calculate_optimal_font_size(text)

        # Create font with optimal size
        if isinstance(settings.OVERLAY_FONT, tuple):
            dynamic_font = (
                self.base_font_family,
                optimal_font_size,
            ) + settings.OVERLAY_FONT[2:]
        else:
            dynamic_font = (self.base_font_family, optimal_font_size)

        # Update label with new font and text
        self.label.config(text=text, font=dynamic_font)

        nb_lines = len(text.split("\n"))
        font_obj = tkfont.Font(font=dynamic_font)
        line_height = font_obj.metrics("linespace")

        # Estimate height based on line count + padding
        padding_vertical = 40  # from pady=20 (top + bottom)
        estimated_height = nb_lines * line_height + padding_vertical
        h = min(estimated_height, self.max_height)

        self.label.config(wraplength=self.max_width - 60)
        self.root.update_idletasks()
        w = min(self.label.winfo_reqwidth(), self.max_width)

        x = self.monitor.x + (self.monitor.width // 2) - (w // 2)
        y = self.monitor.y + int(self.monitor.height * 0.75) - (h // 2)

        self.root.geometry(f"{w}x{h}+{x}+{y}")
        self.root.deiconify()
        self.root.lift()

        self.fade_in()
        self.hide_timer = self.root.after(display_duration_ms, self.fade_out)

    def fade_in(self):
        self.root.wm_attributes("-alpha", self.max_alpha)

    def fade_out(self):
        self.root.wm_attributes("-alpha", 0.0)

        self.root.withdraw()

    def run(self):
        self.root.mainloop()

    def receive(self, message: dict):
        pass
