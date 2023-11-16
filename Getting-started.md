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
  "monitors",
  "shift_monitors",
  "workspaces_follow_focus",
]

[workspaces_follow_focus]
max_workspaces = 9

[monitors]
unknown = "wlrlui"

[monitors.placement]
"PLX2783H-DP".topOf = "DP-1"
"Dell Inc. DELL P24".topOf = "eDP-1"

[scratchpads.volume]
lazy = true
command = "pavucontrol"
unfocus = "hide"
animation = "fromRight"

[scratchpads.term]
command = "kitty --class kitty-dropterm"
animation = "fromTop"
unfocus = "keep"

[scratchpads.stb]
animation = "fromBottom"
lazy = true
command = "kitty --class kitty-stb sstb"

[scratchpads.stb-logs]
animation = "fromTop"
lazy = true
command = "kitty --class kitty-stb-logs stbLog"
```

Which is easy to setup with a couple of bind configuration rules in `hyprland.conf`:

```bash
bind = $mainMod,A,exec,pypr toggle term
bind = $mainMod,V,exec,pypr toggle volume
bind = $mainMod SHIFT,M,exec,pypr toggle stb-logs
bind = $mainMod SHIFT,M,exec,pypr toggle stb
```

> [!note]
> The same `bind` is used twice in this example, this will show one scratch after another, to synchronize several scratches just provide them all to the `toggle` command as in `pypr toggle stb stb-logs`

If you are using animations in `scratchpads`, you may want to consider additional configuration for a better user experience. There are two options, one is to configure `hyprland.conf`, the other is to provide `class` and `size` parameters in the `pyprland.toml` configuration file.

### Pyprland TOML file (option 1)

Complete example:

```ini
[scratchpads.stb]
command = "kitty --class kitty-stb sstb"
class = "kitty-stb"
lazy = true
animation = "fromBottom"
size = "75% 45%"

[scratchpads.stb-logs]
command = "kitty --class kitty-stb-logs stbLog"
class = "kitty-stb-logs"
lazy = true
animation = "fromTop"
size = "75% 40%"

[scratchpads.term]
command = "kitty --class kitty-dropterm"
class = "kitty-dropterm"
animation = "fromTop"
size = "75% 60%"

[scratchpads.volume]
command = "pavucontrol"
class = "pavucontrol"
lazy = true
animation = "fromRight"
size = "40% 90%"
unfocus = "hide"
```

### Hyprland conf (option 2)

Still requires configuring the `command` in `pyprland.toml` (and optional parameters like `animation` if you wish):

```bash
windowrule = float,^(pavucontrol)$
windowrule = size 40% 90%,^(pavucontrol)$
windowrule = move 200% 5%,^(pavucontrol)$
windowrule = workspace special:scratch_volume silent,^(pavucontrol)$

$stblogs = ^(kitty-stb-logs)$
windowrule = float,$stblogs
windowrule = size 75% 25%,$stblogs
windowrule = workspace special:scratch_stb-logs silent,$stblogs

$stb = ^(kitty-stb)$
windowrule = float,$stb
windowrule = size 75% 60%,$stb
windowrule = workspace special:scratch_stb silent,$stb

$dropterm  = ^(kitty-dropterm)$
windowrule = float,$dropterm
windowrule = size 75% 60%,$dropterm
windowrule = move 12% -200%,$dropterm
windowrule = workspace special:scratch_term silent,$dropterm
```

## Troubleshoot

You can enable debug logging and saving to file using the `--debug` argument, eg:

```
pypr --debug /tmp/pypr.log
```

If you just want debug information in the console, set `DEBUG=1` in the environment.
More info in the [troubleshooting](Troubleshooting) page.
