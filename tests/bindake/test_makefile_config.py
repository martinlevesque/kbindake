from bindake.makefile_config import MakefileConfig


def test_makefile_config_happy_path():
    mc = MakefileConfig(filepath="./Makefile.sample")
    bindings = mc.parse()

    assert len(bindings) == 2

    assert bindings["<cmd>+<ctrl>+f"].command == "firefox"
    assert bindings["<cmd>+<ctrl>+f"].autoboot
    assert bindings["<cmd>+<ctrl>+f"].overlay_command_output

    assert bindings["<cmd>+<ctrl>+g"].command == "chrome"
    assert not bindings["<cmd>+<ctrl>+g"].autoboot
    assert not bindings["<cmd>+<ctrl>+g"].overlay_command_output
