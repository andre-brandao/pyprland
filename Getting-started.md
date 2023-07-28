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
    }
    "unknown": "wlrlui"
  }
}
```
