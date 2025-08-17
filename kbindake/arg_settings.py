from dataclasses import dataclass


@dataclass
class ArgSettings:
    verbose: bool = False
    boot_wait: int = 30
    bindings_overlay_hotkey: str = ""
