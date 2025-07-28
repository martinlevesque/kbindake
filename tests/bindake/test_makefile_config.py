from bindake.keyboard import KeyboardKey
from bindake.makefile_config import MakefileConfig


def test_makefile_config_happy_path():
    mc = MakefileConfig(filepath="./Makefile.sample")
    bindings = mc.parse()

    assert len(bindings) == 2

    assert bindings["<cmd>+<shift>+f"].command == "firefox"
    assert bindings["<cmd>+<shift>+f"].autoboot
    assert bindings["<cmd>+<shift>+f"].overlay_command_output

    assert bindings["<cmd>+<shift>+c"].command == "chrome"
    assert not bindings["<cmd>+<shift>+c"].autoboot
    assert not bindings["<cmd>+<shift>+c"].overlay_command_output
