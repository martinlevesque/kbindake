from bindake.keyboard import KeyboardKey
from bindake.makefile_config import MakefileConfig


def test_makefile_config_happy_path():
    mc = MakefileConfig(filepath="./Makefile.sample")
    bindings = mc.parse()

    assert len(bindings) == 2

    assert bindings["Cmd R+Shift+F"].command == "firefox"
    assert bindings["Cmd R+Shift+C"].command == "chrome"
