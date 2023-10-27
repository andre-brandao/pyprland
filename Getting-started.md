Pypr consists in two things:

- **a tool**: `pypr`
- **some config file**: `~/.config/hypr/pyprland.json`

The `pypr` tool only have two built-in commands:

- `reload` reads the configuration file and attempt to apply the changes
- `--help` lists available commands (including plugins commands)

Other commands are added by adding [plugins](Plugins).

The config file uses the following syntax:

```json
{
  "pyprland": {
    "plugins": ["plugin_name"]
  },
  "plugin_name": {
    "plugin_option": 42
  }
}
```

## Installation

Use the python package manager:

```
pip install pyprland
```

If you run archlinux, you can also find it on AUR: `yay -S pyprland`

Don't forget to start the process with hyprland, adding to `hyprland.conf`:

```
exec-once = pypr
```

## Configuring

Create a configuration file in `~/.config/hypr/pyprland.json` enabling a list of plugins, each plugin may have its own configuration needs, eg:

```json
{
  "pyprland": {
    "plugins": [
      "scratchpads",
      "monitors",
      "workspaces_follow_focus"
    ]
  },
  "scratchpads": {
    "term": {
      "command": "kitty --class kitty-dropterm",
      "animation": "fromTop",
      "unfocus": "hide"
    },
    "volume": {
      "command": "pavucontrol",
      "unfocus": "hide",
      "animation": "fromRight"
    }
  },
  "monitors": {
    "placement": {
      "BenQ PJ": {
        "topOf": "eDP-1"
      }
    },
    "unknown": "wlrlui"
  }
}
```
## Troubleshoot

You can enable debug logging and saving to file using the `--debug` argument, eg:

```
pypr --debug /tmp/pypr.log
```

If you just want debug information in the console, set `DEBUG=1` in the environment.
More info in the [troubleshooting](Troubleshooting) page.
