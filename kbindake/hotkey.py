FRIENDLY_HOTKEYS = {"<super>": "<cmd>"}


def normalize_key(key: str) -> str:
    original = key.strip().lower()

    for src, dest in FRIENDLY_HOTKEYS.items():
        if original == src:
            return dest

    return original


def normalize_string_hotkey_to_list(hotkey: str) -> list[str]:
    normalized_hotkey = sorted([normalize_key(k) for k in hotkey.split("+")])

    return normalized_hotkey


def normalize_string_hotkey(hotkey: str) -> str:
    return "+".join(normalize_string_hotkey_to_list(hotkey))
