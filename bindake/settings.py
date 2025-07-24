from dataclasses import dataclass


@dataclass
class Settings:
    verbose: bool = False
    boot_wait: int = 30
