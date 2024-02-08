Presents some menu to run shortcut commands. Supports nested menus (categories / submenus).

Configuration example:

```toml
[shortcuts_menu]
parameters = "--prompt-text 🍰 --fuzzy-match true"
engine = "rofi"

[shortcuts_menu.entries]
"Open Jira ticket" = 'open-jira-ticket "$(wl-paste)"'
"Show Jira cheatsheet" = "xdg-open https://cheatography.com/rhorber/cheat-sheets/jira-text-formatting-notation/"
"WIKI" = "xdg-open http://localhost:8000/"
"Serial USB Term" = "kitty miniterm --raw --eol LF /dev/ttyUSB* 115200"
Gateify = "~/liberty/gatify.sh"
Relayout = "pypr relayout"
```

> [!note]
> **Added in version 1.9.0**

# Command

- `menu [name]`: shows a list of options. If "name" is provided it will show the given sub-menu

# Configuration

## `entries`

Defines the menu entries.

```toml
[shortcuts_menu.entries]
"entry 1" = "command to run"
"entry 2" = "command to run"
```
Submenus can be defined too (there is no depth limit):

```toml
[shortcuts_menu.entries."My submenu"]
"entry X" = "command"

[shortcuts_menu.entries.one.two.three.four.five]
foobar = "ls"
```

## `engine` (optional)

Not set by default, will autodetect the available engine.

Supported engines:

- tofi
- rofi
- wofi
- bemenu
- dmenu

> [!note]
> If your menu system isn't supported, you can open a [feature request](https://github.com/hyprland-community/pyprland/issues/new?assignees=fdev31&labels=bug&projects=&template=feature_request.md&title=%5BFEAT%5D+Description+of+the+feature)

## `parameters` (optional)

Extra parameters added to the engine command, the default value is specific to each engine.

# Hints

## Multiple menus

To manage multiple distinct menus, always use a name when using the `pypr menu <name>` command.

Example of a multi-menu configuration:

```toml
[shortcuts_menu.entries."Basic commands"]
"entry X" = "command"
"entry Y" = "command2"

[shortcuts_menu.entries.menu2]
# ...
```

You can then show menu1 using `pypr menu "Basic commands"`
