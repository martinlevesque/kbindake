import tkinter as tk
from tkinter import font as tkfont
from lib.message_passer import MessagePasser
import settings

class PrinterView(MessagePasser):
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.configure(bg=settings.OVERLAY_BACKGROUND_COLOR)
        self.sw = self.root.winfo_screenwidth()
        self.sh = self.root.winfo_screenheight()
        self.max_width = int(self.sw * 0.9)
        self.max_height = int(self.sh * 0.9)

        # Store base font info for dynamic sizing
        self.base_font_family = settings.OVERLAY_FONT[0] if isinstance(settings.OVERLAY_FONT, tuple) else "Arial"
        self.base_font_size = settings.OVERLAY_FONT[1] if isinstance(settings.OVERLAY_FONT, tuple) else 12

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
        self.root.withdraw()
        self.fade_in_ms = 200
        self.fade_out_ms = 500
        self.max_alpha = 0.85

    def calculate_optimal_font_size(self, text: str):
        """Calculate optimal font size based on text length and screen size"""
        text_length = len(text)
        nb_lines = len(text.split("\n"))

        # Base scaling factors
        if text_length < 100:
            scale_factor = 1.0  # Use original size for short text
        elif text_length < 300:
            scale_factor = 0.85  # Slightly smaller for medium text
        elif text_length < 600:
            scale_factor = 0.7   # Smaller for longer text
        else:
            scale_factor = 0.6   # Much smaller for very long text

        # Additional scaling based on number of lines
        if nb_lines > 10:
            scale_factor *= 0.9
        elif nb_lines > 20:
            scale_factor *= 0.8

        # Calculate new font size
        new_size = max(8, int(self.base_font_size * scale_factor))  # Minimum size of 8

        return new_size

    def show(self, text: str, display_duration_ms: int = 500):
        nb_lines = len(str(text).split("\n"))
        self.root.after(0, self._show_impl, text, display_duration_ms * nb_lines)

    def is_view_destroyed(self):
        try:
            return not self.root.winfo_exists()
        except tk.TclError:
            return True

    def destroy(self):
        if not self.is_view_destroyed():
            self.root.destroy()

    def _show_impl(self, text: str, display_duration_ms: int):
        # Calculate optimal font size for this text
        optimal_font_size = self.calculate_optimal_font_size(text)

        # Create font with optimal size
        if isinstance(settings.OVERLAY_FONT, tuple):
            dynamic_font = (self.base_font_family, optimal_font_size) + settings.OVERLAY_FONT[2:]
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

        x = (self.sw // 2) - (w // 2)
        y = int(self.sh * 0.75) - (h // 2)

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
        pass
