OVERLAY_BACKGROUND_COLOR = "#2e2e2e"
OVERLAY_FONT = ("Segoe UI", 28, "bold")
OVERLAY_MIN_FONT_SIZE = 10
OVERLAY_FONT_COLOR = "#00ffcc"


def overlay_font_size(nb_lines):
    max_font_size = OVERLAY_FONT[1]
    font_size = max(OVERLAY_MIN_FONT_SIZE, int(max_font_size - nb_lines))

    return font_size
