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
animation = "fromTop"
command = "kitty --class kitty-dropterm"
class = "kitty-dropterm"
size = "75% 60%"
max_size = "1920px 100%"
margin = 50
unfocus = "hide"

[scratchpads.volume]
animation = "fromRight"
command = "pavucontrol"
class = "pavucontrol"
size = "40% 90%"
lazy = true
```

Shortcuts are generally needed:

```ini
bind = $mainMod,V,exec,pypr toggle volume
bind = $mainMod,A,exec,pypr toggle term
```

Note that when `class` is provided, the window is automatically managed by pyprland.
When you create a scratchpad called "name", it will be hidden in `special:scratch_<name>`.

# Commands

- `toggle <scratchpad name>` : toggle the given scratchpads (if  more than one name provided, will synchronize status on the first scratchpad)
- `show <scratchpad name>` : show the given scratchpad
- `hide <scratchpad name>` : hide the given scratchpad


# Configuration

## `command`

This is the command you wish to run in the scratchpad.

## `animation` (optional)

Type of animation to use, default value is "fromTop":

- `null` / `""` (no animation)
- "fromTop" (stays close to top screen border)
- "fromBottom" (stays close to bottom screen border)
- "fromLeft" (stays close to left screen border)
- "fromRight" (stays close to right screen border)

## `size` (recommended)

No default value.

Same format as `position` (see above)

Each time scratchpad is shown, window will be resized according to the provided values.

For example on monitor of size `800x600` and `size= "80% 80%"` in config scratchpad always have size `640x480`, regardless of which monitor it was first launched on.

## `class` (recommended)

No default value.

Helps *Pyprland* identify the window for a correct animation.
Required if you are using the `class_match` option.

> [!important]
> This will set some rules to every matching class!

## `unfocus` (optional)

No default value.

When set to `"hide"`, allow to hide the window when the focus is lost.

Use `hysteresis` to change the reactivity

## `hysteresis` (optional)

Defaults to `0.4` (seconds)

Controls how fast a scratchpad hiding on unfocus will react. Check `unfocus` option.
Set to `0` to disable (immediate reaction, as in versions < 2.0.1)

> [!important]
> Only relevant when `unfocus="hide"` is used.

> [!note]
> Added in 2.0.1

## `margin` (optional)

default value is `60`.

number of pixels separating the scratchpad from the screen border, depends on the [animation](#animation) set.

## `lazy` (optional)

default to `false`.

when set to `true`, prevents the command from being started when pypr starts, it will be started when the scratchpad is first used instead.

- Good: saves resources when the scratchpad isn't needed
- Bad: slows down the first display (app has to launch before showing)


## `max_size` (optional)

No default value.

Same format as `position` (see above), only used if `size` is also set.

Limits the `size` of the window accordingly.
To ensure a window will not be too large on a wide screen for instance:

```toml
size = "60% 30%"
max_size = "1200px 100%"
```

## `excludes` (optional)

No default value.

List of scratchpads to hide when this one is displayed, eg: `excludes = ["term", "volume"]`.
If you want to hide every displayed scratch you can set this to the string `"*"` instead of a list: `excludes = "*"`.

## `position` (optional)

No default value, overrides the automatic margin-based position.

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

## `offset` (optional)

In pixels, default to `0` (heuristic value based on the window's size)

number of pixels for the **hide** animation (how far the window will go).

## `restore_focus` (optional)

Enabled by default, set to `false` if you don't want the focused state to be restored when a scratchpad is hidden.

## `class_match` (use only if really needed)

Default value is `false`.

If set to `true`, matches the client window using the provided `WM_CLASS` instead of the PID of the process.

Use it in case of troubles - check [this wiki page](https://github.com/hyprland-community/pyprland/wiki/Troubleshooting#disable-pid-tracking-eg-emacsclient)

Requires `class` to be set to a matching window.

## `process_tracking` (use only if really needed)

Default value is `true`

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
