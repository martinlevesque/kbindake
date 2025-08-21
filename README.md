# kbindake ⚡

> **Hotkey bindings that actually make sense** 🔥
> Use Makefiles to bind keyboard shortcuts to commands. Because why not? 🤷‍♂️

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Platform](https://img.shields.io/badge/platform-cross--platform-green.svg)

## What is this? 🤔

kbindake turns your boring Makefile into a **supercharged hotkey manager**. Press a key combo, run a command, see the output in a slick overlay. It's like having a personal assistant that actually knows what `make` means.

## Features ✨

- 🎯 **Makefile-based configuration** - Reuse your existing build scripts
- 🚀 **Global hotkeys** - Works system-wide, not just in terminal
- 🎨 **Visual overlay** - See command output in beautiful on-screen displays
- ⚡ **Autoboot commands** - Run stuff automatically when kbindake starts
- 🔧 **Live binding viewer** - See all your shortcuts with a special hotkey
- 🎛️ **Flexible options** - Show command output or just the command name

## Quick Start 🏃‍♂️

### Installation

```bash
pip install kbindake  # (when published)
# or
git clone https://github.com/yourusername/kbindake
cd kbindake
pip install -e .
```

### Basic Usage

1. **Create a Makefile** in `~/.config/kbindake/Makefile`:

```makefile
# kbindake: ctrl+alt+t
terminal:
	gnome-terminal

# kbindake[overlay-command-output]: super+d
datetime:
	date "+%Y-%m-%d %H:%M:%S"

# kbindake[autoboot]: ctrl+shift+m
music-setup:
	spotify --minimized &
```

2. **Run kbindake**:

```bash
kbindake
```

3. **Press your hotkeys** and watch the magic happen! ✨

## Configuration Magic 🪄

### Binding Syntax

```makefile
# kbindake[options]: hotkey+combination
command-name:
	your-shell-command-here
```

### Available Options

- `overlay-command-output` - Show command output instead of command name
- `autoboot` - Run this command when kbindake starts

### Examples That'll Blow Your Mind 🤯

```makefile
# Quick screenshot with preview
# kbindake[overlay-command-output]: super+shift+s
screenshot:
	scrot -s ~/Pictures/screenshot_$(date +%s).png && echo "📸 Screenshot saved!"

# System stats overlay
# kbindake[overlay-command-output]: ctrl+alt+i
sysinfo:
	echo "🖥️  CPU: $(top -bn1 | grep "Cpu(s)" | cut -d: -f2 | cut -d, -f1)\n💾 RAM: $(free -h | awk '/^Mem:/ {print $$3 "/" $$2}')"

# Open your favorite editor
# kbindake: ctrl+alt+e
editor:
	code .

# Emergency caffeine level check
# kbindake[overlay-command-output]: alt+c
coffee:
	echo "☕ Time for coffee: $(date)"
```

## Command Line Options 🛠️

```bash
kbindake [options]

Options:
  -v, --verbose                    Enable verbose output (see what's happening)
  -s, --boot-wait N               Wait N seconds before starting (default: 30)
  --bindings-overlay-hotkey KEY   Show current bindings with this hotkey
  --makefile PATH                 Custom Makefile path
```

### Pro Tips 💡

```bash
# See all your bindings
kbindake --bindings-overlay-hotkey="ctrl+shift+h"

# Custom Makefile location
kbindake --makefile ~/my-hotkeys/Makefile

# Debug mode (see what's happening under the hood)
kbindake -v

# Quick start (no boot delay)
kbindake -s 0
```

## Real-World Examples 🌍

### Developer Workflow

```makefile
# kbindake[overlay-command-output]: ctrl+alt+g
git-status:
	git status --porcelain | head -10

# kbindake: ctrl+alt+b
build:
	npm run build

# kbindake[overlay-command-output]: ctrl+alt+p
port-check:
	lsof -ti:3000 || echo "Port 3000 is free! 🎉"
```

### System Management

```makefile
# kbindake[overlay-command-output]: super+shift+w
wifi-info:
	nmcli dev wifi | head -5

# kbindake: ctrl+alt+l
lock-screen:
	gnome-screensaver-command --lock

# kbindake[overlay-command-output]: super+m
memory-usage:
	ps aux --sort=-%mem | head -10
```

## Hotkey Format 📝

- Use `+` to combine keys: `ctrl+alt+t`
- Special keys: `super`, `ctrl`, `alt`, `shift`
- Letters and numbers: `a-z`, `0-9`
- Function keys: `f1`, `f2`, etc.
- Arrow keys: `up`, `down`, `left`, `right`

## Architecture 🏗️

kbindake is built with a clean, modular architecture:

- **MyKeyboard** - Global hotkey detection using `pynput`
- **MakefileConfig** - Parses your Makefile and executes commands
- **PrinterView** - Beautiful overlay system with dynamic sizing
- **MessagePasser** - Event system for component communication

## Alternative Solutions 🔄

kbindake was inspired by these awesome tools:

- [sxhkd](https://github.com/baskerville/sxhkd) - Simple X hotkey daemon
- **xbindkeys** - Classic X11 key binding utility

But kbindake brings the power of **Makefiles** and **cross-platform** support! 🚀

## Contributing 🤝

Found a bug? Want a feature? PRs welcome!

1. Fork it
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License 📄

MIT License - see LICENSE file for details.

---

**Made with ❤️ and too much coffee** ☕

*"Why click when you can hotkey?"* - Ancient developer proverb
