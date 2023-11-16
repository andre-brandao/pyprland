Pypr consists in two things:

- **a tool**: `pypr` which runs the program, but also allows to interract with it
- **some config file**: `~/.config/hypr/pyprland.toml`

The `pypr` tool only have two built-in commands:

- `reload` reads the configuration file and attempt to apply the changes
- `--help` lists available commands (including plugins commands)

> [!note]
> Pypr *command* names are documented using underscores (`_`) but you can use dashes (`-`) instead.
> Eg: `shift_monitors` and `shift-monitors` will run the same command

Other commands are added by adding [plugins](Plugins).

The config file uses the following syntax:

```toml
[pyprland]
plugins = ["plugin_name"]

[plugin_name]
plugin_option = 42

[plugin_name.plugin_option]
suboption = "there is no limit"
```

## Installation

Check your OS package manager first, eg, for archlinux, you can also find it on AUR: `yay -S pyprland`

Otherwise, use the python package manager *inside a virtual environment* (`python -m venv somefolder && source ./somefolder/bin/activate`):

```
pip install pyprland
```


Don't forget to start the process with hyprland, adding to `hyprland.conf`:

```
exec-once = pypr
```

## Configuring

Create a configuration file in `~/.config/hypr/pyprland.toml` enabling a list of plugins, each plugin may have its own configuration needs or don't need any configuration at all. Most default values should be okay, just set when you are not satisfied with the default.

Check the [TOML format](https://toml.io/) for details about the syntax.
Example:

```toml
[pyprland]
plugins = [
  "scratchpads",
  "lost_windows",
  "monitors",
  "shift_monitors",
  "toggle_dpms",
  "magnify",
  "expose",
  "shift_monitors",
  "workspaces_follow_focus",
]

[workspaces_follow_focus]
max_workspaces = 9

[expose]
include_special = false

[scratchpads.stb]
animation = "fromBottom"
command = "kitty --class kitty-stb sstb"
class = "kitty-stb"
lazy = true
size = "75% 45%"

[scratchpads.stb-logs]
animation = "fromTop"
command = "kitty --class kitty-stb-logs stbLog"
class = "kitty-stb-logs"
lazy = true
size = "75% 40%"

[scratchpads.term]
animation = "fromTop"
command = "kitty --class kitty-dropterm"
class = "kitty-dropterm"
size = "75% 60%"

[scratchpads.volume]
animation = "fromRight"
command = "pavucontrol"
class = "pavucontrol"
lazy = true
size = "40% 90%"
unfocus = "hide"

[monitors]
unknown = "wlrlui"

[monitors.placement]
"Acer".leftOf = "HDMI-0"
"Sony".topOf = "eDP-1"
```

Which is easy to use with a couple of bind configuration rules in `hyprland.conf`, eg:

```bash
bind = $mainMod , N, exec, pypr toggle_minimized
bind = $mainMod SHIFT, Z, exec, pypr zoom
bind = $mainMod ALT, P,exec, pypr toggle_dpms
bind = $mainMod SHIFT, O, exec, pypr shift_monitors +1
bind = $mainMod, B, exec, pypr expose
bind = $mainMod, K, exec, pypr change_workspace +1
bind = $mainMod, J, exec, pypr change_workspace -1
bind = $mainMod,L,exec, pypr toggle_dpms
bind = $mainMod SHIFT,M,exec,pypr toggle stb stb-logs
bind = $mainMod,A,exec,pypr toggle term
bind = $mainMod,V,exec,pypr toggle volume
```

## Troubleshoot

You can enable debug logging and saving to file using the `--debug` argument, eg:

```
pypr --debug /tmp/pypr.log
```

If you just want debug information in the console, set `DEBUG=1` in the environment.
More info in the [troubleshooting](Troubleshooting) page.
