from kbindake import hotkey


def test_hotkey_normalize_hotkey_happy_path():
    assert hotkey.normalize_string_hotkey("<Shift>+<Cmd>+f") == "<cmd>+<shift>+f"


def test_hotkey_normalize_hotkey_identical():
    assert hotkey.normalize_string_hotkey("<cmd>+<shift>+f") == "<cmd>+<shift>+f"


def test_hotkey_normalize_hotkey_friendly_hotkey():
    assert hotkey.normalize_string_hotkey("<super>+<shift>+f") == "<cmd>+<shift>+f"


def test_hotkey_normalize_hotkey_empty():
    assert hotkey.normalize_string_hotkey("") == ""
