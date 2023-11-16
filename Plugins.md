You may install more plugins by using 3rd party or custom Python packages.
Pyprland provides the following plugins out of the box:

- 🌟🌟🌟 [scratchpads](#scratchpads) implements dropdowns & togglable poppups
    [![demo video](https://img.youtube.com/vi/ZOhv59VYqkc/0.jpg)](https://www.youtube.com/watch?v=ZOhv59VYqkc)
- 🌟🌟 [monitors](#monitors) allows relative placement of monitors depending on the model
- 🌟 [expose](#expose) easily switch between scratchpads and active workspace:
    [![demo video](https://img.youtube.com/vi/ce5HQZ3na8M/0.jpg)](https://www.youtube.com/watch?v=ce5HQZ3na8M)
    [![demo video](https://img.youtube.com/vi/BNZCMqkwTOo/0.jpg)](https://www.youtube.com/watch?v=BNZCMqkwTOo)
- 🌟🌟🌟 [workspaces_follow_focus](#workspaces_follow_focus) provides commands and handlers allowing a more flexible workspaces usage on multi-monitor setups. If you think the multi-screen behavior of hyprland is not usable or broken/unexpected, this is probably for you.
- [lost_windows](#lost_windows) brings lost floating windows (which are out of reach) to the current workspace
- [toggle_dpms](#toggle_dpms) toggles the DPMS status of every plugged monitor
- 🌟🌟🌟 [magnify](#magnify) toggles zooming of viewport or sets a specific scaling factor
    [![demo video](https://img.youtube.com/vi/yN-mhh9aDuo/0.jpg)](https://www.youtube.com/watch?v=yN-mhh9aDuo)
- 🌟🌟 [shift_monitors](#shift_monitors) adds a self-configured "swapactiveworkspaces" command


> [!note]
> "🌟" indicates some maturity & reliability level of the plugin, considering age, attention paid and complexity - from 0 to 3.


# `shift_monitors`

Swaps the workspaces of every screen in the given direction.

> [!Note]
> the behavior can be hard to predict if you have more than 2 monitors (depending on your layout).
> If you use this plugin with many monitors and have some ideas about a convenient configuration, you are welcome ;)

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


#### `factor` (optional)

defaults to `2`

Scaling factor to be used when no value is provided.

# `toggle_dpms`

### Command

- `toggle_dpms`: if any screen is powered on, turn them all off, else turn them all on


# `lost_windows`

### Command

- `attract_lost`: brings the lost windows to the current screen / workspace

# `monitors`

Allows relative placement of monitors depending on the model ("description" returned by `hyprctl monitors`).
Useful if you have multiple monitors connected to a video signal switch or using a laptop and plugging monitors having different relative positions.

Requires `wlr-randr`.

Syntax:
```toml
[monitors]
unknown = "program to run"

[monitors.placement]
"description match".placement = "output"
```

Example to set a Sony monitor on top of the one plugged in "HDMI-1":
```toml
[monitors.placement]
Sony.topOf = "HDMI-1"
```

> [!note]
> Check [wlr layout UI](https://github.com/fdev31/wlr-layout-ui) which is a great complement to configure your monitor settings.

### Configuration


#### `placement`

Supported placements are:

- leftOf
- topOf
- rightOf
- bottomOf

#### `unknown` (optional)

If set, runs the associated command for screens which aren't matching any of the provided placements (pattern isn't found in monitor description).

> [!warning]
> this is supposed to be a short lived command which will block the rest of the process until closed. In other words no plugin will be processed while this command remains open.

# `workspaces_follow_focus`

Make non-visible workspaces follow the focused monitor.
Also provides commands to switch between workspaces wile preserving the current monitor assignments: 

Syntax:
```toml
[workspaces_follow_focus]
max_workspaces = 4 # number of workspaces before cycling
```

### Command

- `change_workspace` `<direction>`: changes the workspace of the focused monitor

Example usage in `hyprland.conf`:

```
bind = $mainMod, K, exec, pypr change_workspace +1
bind = $mainMod, J, exec, pypr change_workspace -1
 ```

### Configuration

#### `max_workspaces`

Limits the number of workspaces when switching, defaults to `10`.

# `scratchpads`

Defines commands that should run in dropdowns. Successor of [hpr-scratcher](https://github.com/hyprland-community/hpr-scratcher), it's fully compatible, just put the configuration under "scratchpads".

Syntax:
```toml
[scratchpads.name]
command = "command to run"
```

As an example, defining two scratchpads:

- _term_ which would be a kitty terminal on upper part of the screen
- _volume_ which would be a pavucontrol window on the right part of the screen

Example:
```toml
[scratchpads.term]
command = "kitty --class kitty-dropterm"
animation = "fromTop"
margin = 50
unfocus = "hide"

[scratchpads.volume]
command = "pavucontrol"
animation = "fromRight"
```

In your `hyprland.conf` you may want to set the scratchpad apps as floating and optionally resize them and set the initial special workspace name (format: `special:scratch_<name>`) to get an optimal display, eg:

```ini
exec-once = pypr

# Repeat this for each scratchpad you need
bind = $mainMod,V,exec,pypr toggle volume
windowrule = float,^(pavucontrol)$
windowrule = size 40% 90%,^(pavucontrol)$
windowrule = move 200% 5%,^(pavucontrol)$
windowrule = workspace special:scratch_volume silent,^(pavucontrol)$

bind = $mainMod,A,exec,pypr toggle term
$dropterm  = ^(kitty-dropterm)$
windowrule = float,$dropterm
windowrule = workspace special:scratch_term silent,$dropterm
windowrule = size 75% 60%,$dropterm
windowrule = move 12% -200%,$dropterm
```

And you'll be able to toggle pavucontrol with `MOD + V` and kitty with `MOD + A`.

### Commands

- `toggle <scratchpad name>` : toggle the given scratchpads (if  more than one name provided, will synchronize status on the first scratchpad)
- `show <scratchpad name>` : show the given scratchpad
- `hide <scratchpad name>` : hide the given scratchpad

> [!important]
> with no argument it runs the daemon (doesn't fork in the background)



### Configuration

#### `command`

This is the command you wish to run in the scratchpad.

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


#### `size` (optional)

string in format `"X% Y%"`, where X and Y is percentage of monitor's width and height accordingly. Every time scratchpad is shown, window will be resized depending on the monitor size, it displayed on.
For example on monitor of size `800x600` and `size= "80% 80%"` in config scratchpad always have size `640x480`, regardless of which monitor it was first launched on.

#### `position` (optional)

every time scratchpad is shown, window will be moved to specified position relative to top left corner. For format and example see `size`.

example of scratchpad that always occupy top half of the screen:
```toml
[scratchpads.term_quake]
command = "wezterm start --class term_quake"
position = "0% 0%"
size = "100% 50%"
```

#### `class` (optional)

Match the client window using the provided `WM_CLASS` instead of the PID of the process.
Use it in case of troubles - check [this wiki page](https://github.com/hyprland-community/pyprland/wiki/Troubleshooting#disable-pid-tracking-eg-emacsclient)

#### `excludes` (optional)

List of scratchpads to hide when this one is displayed, eg: `excludes = ["term", "volume"]`.
If you want to hide every displayed scratch you can set this to the string `"*"` instead of a list: `excludes = "*"`.
