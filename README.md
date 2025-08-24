# kbindake

> **Hotkey bindings that actually make sense** 🔥
> Use Makefiles to bind keyboard shortcuts to commands.

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![Platform](https://img.shields.io/badge/platform-cross--platform-green.svg)

## Overview

kbindake turns your Makefile into a **supercharged hotkey manager**. kbindake allows to map key combos into makefile commands, and see the output in a convenient overlay.

## Features ✨

- 🎯 **Makefile-based configuration** - Reuse your existing makefile scripts.
- 🚀 **Global hotkeys** - Works system-wide, allows to switch between programs efficiently with a keybinding.
- 🎨 **Visual overlay** - See command output in beautiful on-screen displays.
- ⚡ **Autoboot commands** - Run stuff automatically when kbindake starts.
- 🔧 **Help binding viewer** - See all your shortcuts with a special hotkey.

## Quick Start

### Installation

```bash
git clone https://github.com/martinlevesque/kbindake
cd kbindake
pip install -r requirements.txt
```

### Basic Usage

1. **Create a Makefile** in `~/.config/kbindake/Makefile`:

```makefile
# kbindake[autoboot,overlay-command-output]: <Super>+<Ctrl>+f
firefox:
	firefox &
```

This sample Makefile will boot a new instance of firefox when hitting Super+Ctrl+F. Note that, to make it resumable and avoid booting a new firefox process everytime, you can reuse it with a command such as (example in Linux):

```makefile
# kbindake[autoboot,overlay-command-output]: <Super>+<Ctrl>+f
firefox:
	if pgrep -x firefox-bin > /dev/null; then \
		wmctrl -xa firefox; \
	else \
		firefox & \
	fi; \
	echo "Firefox Browser"
```

The overlay-command-ouput specifies that the stdout output is displayed in the UI overlay, in this example it will be display "Firefox Browser".
See an example in `Makefile.sample`.

2. **Run kbindake manually for testing**:

```bash
python kbindake/main.py -v
```

3. **Make it autoboot**

Add the command line into your favorite startup application manager (e.g. Startup Applications Preferences in Ubuntu):

```
python <kbindake folder>/kbindake/main.py --boot-wait 30 --bindings-overlay-hotkey "<Super>+h"
```

The `--boot-wait` option is recommended such that the graphical interface has been initialized at boot time.

## Hotkey Format 📝

- Use `+` to combine keys: `<ctrl>+<alt>+t`
- Special keys: `<super>`, `<ctrl>`, `<alt>`, `<shift>`
- Letters and numbers: `a-z`, `0-9`
- Function keys: `<f1>`, `<f2>`, etc.
- Arrow keys: `<up>`, `<down>`, `<left>`, `<right>`

## Implementation structure

kbindake is built with a simple, modular architecture:

- **`kbindake/keyboard.py`** - Global hotkey detection using `pynput`.
- **`kbindake/makefile_config.py`** - Parses your Makefile and executes commands.
- **`kbindake/printer_view.py`** - Overlay UI component with dynamic sizing.
- **`kbindake/__init__.py`** - Glue the 3 main modules together.

## Alternative Solutions

kbindake was inspired by these awesome tools:

- [sxhkd](https://github.com/baskerville/sxhkd) - Simple X hotkey daemon
- **xbindkeys** - Classic X11 key binding utility

## Contributing 🤝

Found a bug? Want a feature? PRs welcome!

1. Fork it
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

*"Why click when you can hotkey?"* - Some ancient developer proverb
