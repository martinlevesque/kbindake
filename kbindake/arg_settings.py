from dataclasses import dataclass


@dataclass
class ArgSettings:
    verbose: bool = False
    boot_wait: int = 0
    bindings_overlay_hotkey: str = ""
    makefile: str = ""
