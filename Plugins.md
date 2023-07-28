You may install more plugins by using 3rd party or custom Python packages.
Pyprland provides the following plugins out of the box:

- `scratchpads` implements dropdowns & togglable poppups
    [![demo video](https://img.youtube.com/vi/ZOhv59VYqkc/0.jpg)](https://www.youtube.com/watch?v=ZOhv59VYqkc)
- `monitors` allows relative placement of monitors depending on the model
- `expose` easily switch between scratchpads and active workspace :
    [![demo video](https://img.youtube.com/vi/ce5HQZ3na8M/0.jpg)](https://www.youtube.com/watch?v=ce5HQZ3na8M)
    [![demo video](https://img.youtube.com/vi/BNZCMqkwTOo/0.jpg)](https://www.youtube.com/watch?v=BNZCMqkwTOo)
- `workspaces_follow_focus` provides commands and handlers allowing a more flexible workspaces usage on multi-monitor setups. If you think the multi-screen behavior of hyprland is not usable or broken/unexpected, this is probably for you.
- `lost_windows` brings lost floating windows to the current workspace
- `toggle_dpms` toggles the DPMS status of every plugged monitor
- `magnify` toggles zooming of viewport or sets a specific scaling factor
    [![demo video](https://img.youtube.com/vi/yN-mhh9aDuo/0.jpg)](https://www.youtube.com/watch?v=yN-mhh9aDuo)
- `shift_monitors` adds a self-configured "swapactiveworkspaces" command


# `expose`

Moves the focused window to some (hidden) special workspace and back with one command.

### Command

- `toggle_minimized [name]`: moves the focused window to the special workspace "name", or move it back to the active workspace.
    If none set, special workspace "minimized" will be used.
- `expose`: expose every client on the active workspace. If expose is active restores everything and move to the focused window

Example usage in `hyprland.conf`:

```
bind = $mainMod, N, exec, pypr toggle_minimized
 ```

### Configuration


#### `include_special` (optional, defaults to false)

Also include windows in the special workspaces during the expose.


# `shift_monitors`

Swaps the workspaces of every screen in the given direction.
Note the behavior can be hard to predict if you have more than 2 monitors, suggestions are welcome.

### Command

- `shift_monitors <direction>`: swaps every monitor's workspace in the given direction

Example usage in `hyprland.conf`:

```
bind = $mainMod SHIFT, O, exec, pypr shift_monitors +1
 ```

# `magnify`

### Command

- `zoom [value]`: if no value, toggles magnification. If an integer is provided, it will set as scaling factor.

### Configuration


#### `factor` (optional, defaults to 2)

Scaling factor to be used when no value is provided.

# `toggle_dpms`

### Command

- `toggle_dpms`: if any screen is powered on, turn them all off, else turn them all on


# `lost_windows`

### Command

- `attract_lost`: brings the lost windows to the current screen / workspace

# `monitors`

Syntax:
```json
"monitors": {
  "placement": {
    "<partial model description>": {
      "placement type": "<monitor name/output>"
    },
    "unknown": "<command to run for unknown monitors>"
  }
}
```

Example:
```json
"monitors": {
  "unknown": "notify-send 'Unknown monitor'",
  "placement": {
    "Sony": {
      "topOf": "HDMI-1"
    }
  }
}
```

Requires `wlr-randr`.

Allows relative placement of monitors depending on the model ("description" returned by `hyprctl monitors`).

### Configuration


#### `placement`

Supported placements are:

- leftOf
- topOf
- rightOf
- bottomOf

#### `unknown` (optional)

If set, runs the associated command for screens which aren't matching any of the provided placements (pattern isn't found in monitor description).

**Note** this is supposed to be a short lived command which will block the rest of the process until closed. In other words no plugin will be processed while this command remains open.

# `workspaces_follow_focus`

Make non-visible workspaces follow the focused monitor.
Also provides commands to switch between workspaces wile preserving the current monitor assignments: 

Syntax:
```json
"workspaces_follow_focus": {
  "max_workspaces": <number of workspaces>
}
```

### Command

- `change_workspace` `<direction>`: changes the workspace of the focused monitor

Example usage in `hyprland.conf`:

```
bind = $mainMod, K, exec, pypr change_workspace +1
bind = $mainMod, J, exec, pypr change_workspace -1
 ```

### Configuration

You can set the `max_workspaces` property, defaults to `10`.

# `scratchpads`

Defines commands that should run in dropdowns. Successor of [hpr-scratcher](https://github.com/hyprland-community/hpr-scratcher), it's fully compatible, just put the configuration under "scratchpads".

Syntax:
```json
"scratchpads": {
  "scratchpad name": {
    "command": "command to run"
  }
}
```

As an example, defining two scratchpads:

- _term_ which would be a kitty terminal on upper part of the screen
- _volume_ which would be a pavucontrol window on the right part of the screen

Example:
```json
"scratchpads": {
  "term": {
    "command": "kitty --class kitty-dropterm",
    "animation": "fromTop",
    "margin": 50,
    "unfocus": "hide"
  },
  "volume": {
    "command": "pavucontrol",
    "animation": "fromRight"
  }
}
```

In your `hyprland.conf` add something like this:

```ini
exec-once = pypr

# Repeat this for each scratchpad you need
bind = $mainMod,V,exec,pypr toggle volume
windowrule = float,^(pavucontrol)$
windowrule = workspace special silent,^(pavucontrol)$

bind = $mainMod,A,exec,pypr toggle term
$dropterm  = ^(kitty-dropterm)$
windowrule = float,$dropterm
windowrule = workspace special silent,$dropterm
windowrule = size 75% 60%,$dropterm
```

And you'll be able to toggle pavucontrol with MOD + V.

### Commands

- `toggle <scratchpad name>` : toggle the given scratchpad
- `show <scratchpad name>` : show the given scratchpad
- `hide <scratchpad name>` : hide the given scratchpad

Note: with no argument it runs the daemon (doesn't fork in the background)



### Configuration

#### `command`

This is the command you wish to run in the scratchpad.
For a nice startup you need to be able to identify this window in `hyprland.conf`, using `--class` is often a good idea.

#### `animation` (optional)

Type of animation to use

- `null` / `""` / not defined (no animation)
- "fromTop" (stays close to top screen border)
- "fromBottom" (stays close to bottom screen border)
- "fromLeft" (stays close to left screen border)
- "fromRight" (stays close to right screen border)

#### `offset` (optional)

number of pixels for the animation.

#### `unfocus` (optional)

when set to `true`, allow to hide the window when the focus is lost when set to "hide"

#### `margin` (optional)

number of pixels separating the scratchpad from the screen border

#### `lazy` (optional)

when set to `true`, prevents the command from being started when pypr starts, it will be started when the scratchpad is first used instead.
