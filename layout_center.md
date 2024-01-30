Implements a workspace layout where one window is bigger and centered,
other windows are tiled as usual in the background.

On `toggle`, the active window is made floating and centered if the layout wasn't enabled, else reverts the floating status.

With `next` and `prev` you can cycle the active window, keeping the same layout type.
If the layout_center isn't active and `next` or `prev` is used, it will change the focus in the "right" or "left" direction.
This allows keeping the same keyboard binding to change the focus regardless of the status of this layout.
If you prefer a vertical ("up" and "down") focus override, enable the `vertical` configuration option (described below).

Sample usage in `hyprland.conf`:
```sh
bind = $mainMod, M, exec, pypr layout_center toggle
bind = $mainMod, left, exec, pypr layout_center prev
bind = $mainMod, right, exec, pypr layout_center next
bind = $mainMod, up, movefocus, u
bind = $mainMod, down, movefocus, d
```

# Command

- `layout_center [command]` where *[command]* can be:
  - next
  - prev
  - toggle

# Configuration

## `vertical` (optional)

If the *layout_center* isn't active, trigger focus "up" or "down" instead of "left" and "right".

## `margin` (optional)

defaults to `100`

margin used when placing the center window, calculated from the border of the screen.

> [!note]
> **Added in version 1.8.0**
