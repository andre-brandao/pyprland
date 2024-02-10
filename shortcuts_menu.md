Presents some menu to run shortcut commands. Supports nested menus (categories / submenus).

Configuration example:

```toml
[shortcuts_menu]
parameters = "--prompt-text 🍰 --fuzzy-match true"
engine = "rofi"

[shortcuts_menu.entries]
"Open Jira ticket" = 'open-jira-ticket "$(wl-paste)"'
"Show Jira cheatsheet" = "xdg-open https://cheatography.com/rhorber/cheat-sheets/jira-text-formatting-notation/"
"Local WIKI" = "xdg-open http://localhost:8000/"
"Serial USB Term" = "kitty miniterm --raw --eol LF /dev/ttyUSB* 115200"
Custom = "~/scripts/custom.sh"
Relayout = "pypr relayout"
"Hyprland socket" = 'kitty  socat - "UNIX-CONNECT:/tmp/hypr/$HYPRLAND_INSTANCE_SIGNATURE/.socket2.sock"'
"Hyprland logs" = 'kitty tail -f /tmp/hypr/$HYPRLAND_INSTANCE_SIGNATURE/hyprland.log'
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

### Advanced usage (since version 1.10)

Instead of navigating a configured list of menu options and running a pre-defined command, you can collect various *variables* (either static list of options selected by the user, or generated from a shell command) and then run a command using those variables. Eg:

```toml
"Play Video" = [
    {var="video_device", command="ls /dev/video*"},
    {var="player", options=["mpv", "vlc"]},
    "{player} {video_device}"
    ]
```

You must define a list of objects, containing:
- `var`: the variable name
- `options` for a static list of options
- `command` to get the list of options from a shell command's output
the last item of the list must be a string which is the command to run. Variables can be used enclosed in `{}`.

## `engine` (optional)

Not set by default, will autodetect the available menu engine.

Supported engines:

- tofi
- rofi
- wofi
- bemenu
- dmenu

> [!note]
> If your menu system isn't supported, you can open a [feature request](https://github.com/hyprland-community/pyprland/issues/new?assignees=fdev31&labels=bug&projects=&template=feature_request.md&title=%5BFEAT%5D+Description+of+the+feature)
>
> In case the engine isn't recognized, `engine` + `parameters` configuration options will be used to start the process, it requires a dmenu-like behavior.

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

You can then show the first menu using `pypr menu "Basic commands"`
