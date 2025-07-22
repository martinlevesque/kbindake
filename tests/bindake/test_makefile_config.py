from bindake.keyboard import KeyboardKey
from bindake.makefile_config import MakefileConfig


def test_makefile_config_happy_path():
    mc = MakefileConfig(filepath="./Makefile.sample")
    bindings = mc.parse()

    assert len(bindings) == 2

    print(f"{bindings}")
    assert bindings["cmd r+f+shift r"].command == "firefox"
    assert bindings["c+cmd r+shift r"].command == "chrome"
