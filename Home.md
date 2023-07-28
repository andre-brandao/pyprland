# Welcome to the pyprland wiki!

## Pyprland is an hyprland companion app enabling Scratchpads, smart monitor placement and other tweaks.
Check the [plugin list](Plugins) for the full list of features.
It consists in two things:

- **a tool**: `pypr`
- **some config file**: `~/.config/hypr/pyprland.json`

The `pypr` tool only have two built-in commands:

- `reload` reads the configuration file and attempt to apply the changes
- `--help` lists available commands (including plugins commands)

Other commands are added by adding plugins.

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