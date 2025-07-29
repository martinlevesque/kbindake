def normalize_string_hotkey_to_list(hotkey: str) -> list[str]:
    normalized_hotkey = sorted([k.strip().lower() for k in hotkey.split("+")])

    return normalized_hotkey


def normalize_string_hotkey(hotkey: str) -> str:
    return "+".join(normalize_string_hotkey_to_list(hotkey))
