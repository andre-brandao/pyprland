You may install more plugins by using 3rd party or custom Python packages.

Pyprland provides the following plugins:

- 🌟🌟🌟 [scratchpads](#scratchpads) implements dropdowns & togglable poppups
    [![demo video](https://img.youtube.com/vi/ZOhv59VYqkc/0.jpg)](https://www.youtube.com/watch?v=ZOhv59VYqkc)
- 🌟🌟🌟 [workspaces_follow_focus](#workspaces_follow_focus) provides commands and handlers allowing a more flexible workspaces usage on multi-monitor setups. If you think the multi-screen behavior of hyprland is not usable or broken/unexpected, this is probably for you.
- 🌟🌟🌟 [magnify](#magnify) toggles zooming of viewport or sets a specific scaling factor
    [![demo video](https://img.youtube.com/vi/yN-mhh9aDuo/0.jpg)](https://www.youtube.com/watch?v=yN-mhh9aDuo)
- 🌟🌟🌟 [shift_monitors](#shift_monitors) adds a self-configured "swapactiveworkspaces" command
- 🌟🌟🌟 [monitors](#monitors) allows relative placement of monitors depending on the model
- 🌟 [expose](#expose) easily switch between scratchpads and active workspace:
    [![demo video](https://img.youtube.com/vi/ce5HQZ3na8M/0.jpg)](https://www.youtube.com/watch?v=ce5HQZ3na8M)
    [![demo video](https://img.youtube.com/vi/BNZCMqkwTOo/0.jpg)](https://www.youtube.com/watch?v=BNZCMqkwTOo)
- [lost_windows](#lost_windows) brings lost floating windows (which are out of reach) to the current workspace
- [toggle_dpms](#toggle_dpms) toggles the DPMS status of every plugged monitor


> [!note]
> "🌟" indicates some maturity & reliability level of the plugin, considering age, attention paid and complexity - from 0 to 3.

# `expose`

This plugin have two features:

The two commands are not really related, one allows the "expose" effect, showing every client window on the focused screen.
The other one allows you to have some kind of dynamic scratchpad, which can be used to minimize (and back) the windows.
They have in common the way they display the client windows to "restore" or "focus" to a specific one.

Sample `hyprland.conf`:

*toggle_minimized feature:*
```bash
bind = $mainMod SHIFT, U, togglespecialworkspace, minimized
bind = $mainMod, N, exec, pypr toggle_minimized
```

No other configuration needed, here `MOD+SHIFT+U` will show every "minimized" clients, while `MOD+N` will (un)minimize the focused client.

*expose feature:*
```bash
bind = $mainMod, B, exec, pypr expose
```
`MOD+B` will bring every client to the focused workspace, pressed again it will go to this workspace.

### Commands

- `toggle_minimized [name]`: moves the focused window to the special workspace "name", or move it back to the active workspace.
    If none set, a special workspace called "minimized" will be used.
    To toggle the state back to a normal workspace, you'll need to `hyprctl dispatch togglespecialworkspace minimized` (if you didn't set a name, since "minimized" is the default special workspace that will be used).
    It can also be achieved with a keybinding: `bind = $mainMod SHIFT, N, togglespecialworkspace, minimized` in `hyprland.conf`

- `expose`: expose every client on the active workspace. If expose is already active, then restores everything and move to the focused window.

Example usage in `hyprland.conf`:

```
bind = $mainMod, N, exec, pypr toggle_minimized
 ```

### Configuration


#### `include_special` (optional)

defaults to `false`

Also include windows in the special workspaces during the expose.


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

> [!note]
> First version of the plugin is still available under the name `monitors_v0`

Allows relative placement of monitors depending on the model ("description" returned by `hyprctl monitors`).
Useful if you have multiple monitors connected to a video signal switch or using a laptop and plugging monitors having different relative positions.

Requires `wlr-randr`.

Syntax:
```toml
[monitors]
unknown = "program to run"

[monitors.placement]
"description match".placement = ["other monitor description", "another monitor name"]
```

Example to set a Sony monitor on top of the BenQ monitor:
```toml
[monitors.placement]
Sony.topOf = ["BenQ"]
# Same as (case is ignored, "_" can be added)
# Sony.Top_Of = ["BenQ"]
"XYZ brand".leftOf = ["Sony", "BenQ"]
```

> [!note]
> Check [wlr layout UI](https://github.com/fdev31/wlr-layout-ui) which is a nice complement to configure your monitor settings.

### Configuration


#### `placement`

Supported placements are:

- leftOf
- topOf
- rightOf
- bottomOf
- \<one of the above>(center|middle|end)Of *

> \* If you don't like the screen to align on the start of the given border, you can use `center` (or `middle`) to center it or `end` to stick it to the opposite border.
> Eg: "topCenterOf", "leftEndOf", etc...


#### `unknown` (optional)

If set, runs the associated command for screens which aren't matching any of the provided placements (pattern isn't found in monitor description).

> [!warning]
> this is supposed to be a short lived command which will block the rest of the process until closed. In other words no plugin will be processed while this command remains open.

# `workspaces_follow_focus`

Make non-visible workspaces follow the focused monitor.
Also provides commands to switch between workspaces while preserving the current monitor assignments: 

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
size = "75% 60%"
max_size = "1920px 100%"

[scratchpads.volume]
command = "pavucontrol"
animation = "fromRight"
class = "pavucontrol"
lazy = true
size = "40% 90%"
```

In case you can't use `class` and `size`, you may need to edit your `hyprland.conf` to set the scratchpad apps as floating and optionally resize them and set the initial special workspace name (format: `special:scratch_<name>`) to get an optimal display, eg:

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

It also binds some shortcuts to use the dropdowns, which you'll probably need.

### Commands

- `toggle <scratchpad name>` : toggle the given scratchpads (if  more than one name provided, will synchronize status on the first scratchpad)
- `show <scratchpad name>` : show the given scratchpad
- `hide <scratchpad name>` : hide the given scratchpad


### Configuration

#### `command`

This is the command you wish to run in the scratchpad.

#### `animation` (optional - RECOMMENDED)

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

number of pixels separating the scratchpad from the screen border, depends on the [animation](#animation) set.

#### `lazy` (optional)

when set to `true`, prevents the command from being started when pypr starts, it will be started when the scratchpad is first used instead.

- Pro: saves resources when the scratchpad isn't needed
- Con: slows down the first display (app has to launch first)

#### `position` (optional)

Sets the scratchpad client window position relative to the top-left corner.

**Format**

String with "x y" values using units suffix:

- **percents** relative to the focused screen size (`%` suffix), eg: `60% 30%`
- **pixels** for absolute values (`px` suffix), eg: `800px 600px`
- a mix is possible, eg: `800px 40%`

Example of scratchpad that always seat on the top-right corner of the screen:

```toml
[scratchpads.term_quake]
command = "wezterm start --class term_quake"
position = "50% 0%"
size = "50% 50%"
class = "term_quake"
```

> [!note]
> If `position` is not provided, the window is placed according to `margin` on one axis and centered on the other.

#### `size` (optional - RECOMMENDED)

Same format as `position` (see above)

Each time scratchpad is shown, window will be resized according to the provided values.

For example on monitor of size `800x600` and `size= "80% 80%"` in config scratchpad always have size `640x480`, regardless of which monitor it was first launched on.

#### `max_size` (optional)

Same format as `position` (see above), only used if `size` is also set.

Limits the `size` of the window accordingly.
To ensure a window will not be too large on a wide screen for instance:

```toml
size = "60% 30%"
max_size = "1200px 100%"
```

#### `class` (optional - RECOMMENDED)

Helps *Pyprland* identify the window for a correct animation.
Required if you are using the `class_match` option.

> [!warning]
> This will set some rules to every matching class !

#### `class_match` (optional)

If set to `true`, matches the client window using the provided `WM_CLASS` instead of the PID of the process.

Use it in case of troubles - check [this wiki page](https://github.com/hyprland-community/pyprland/wiki/Troubleshooting#disable-pid-tracking-eg-emacsclient)

Requires `class` to be set to a matching window.

#### `excludes` (optional)

List of scratchpads to hide when this one is displayed, eg: `excludes = ["term", "volume"]`.
If you want to hide every displayed scratch you can set this to the string `"*"` instead of a list: `excludes = "*"`.

#### `process_tracking` (optional - DISCOURAGED)

Allows disabling the process management. Use only if running a progressive web app (Chrome based apps) or similar.
Check [this wiki page](https://github.com/hyprland-community/pyprland/wiki/Troubleshooting#disable-process-management) for some details.

This will automatically force `lazy = false` and `class_match = true` to help with the fuzzy client window matching.

It requires defining a `class` option.

Eg:

```toml
[scratchpads.music]
command = "google-chrome --profile-directory=Default --app-id=cinhimbnkkaeohfgghhklpknlkffjgod"
class = "chrome-cinhimbnkkaeohfgghhklpknlkffjgod-Default"
size = "50% 50%"
process_tracking = false
```
