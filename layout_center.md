Implements a workspace layout where one window is bigger and centered,
other windows are tiled as usual in the background.

On `toggle`, the active window is made floating and centered if the layout wasn't enabled, else reverts the floating status.

With `next` and `prev` you can cycle the active window, keeping the same layout type.
If the layout_center isn't active and `next` or `prev` is used, it will call the "next" and "prev" configuration options.
To allow full override of the focus keys, `next2` and `prev2` are provided, they do the same actions as "next" and "prev" but allow different fallback commands.

Configuration sample:
```toml
[layout_center]
margin = 60
offset = "0 30"
next = "movefocus r"
prev = "movefocus l"
next2 = "movefocus d"
prev2 = "movefocus u"
```

using the following in `hyprland.conf`:
```sh
bind = $mainMod, M, exec, pypr layout_center toggle # toggle the layout
# focus change keys
bind = $mainMod, left, exec, pypr layout_center prev
bind = $mainMod, right, exec, pypr layout_center next
bind = $mainMod, up, exec, pypr layout_center prev2
bind = $mainMod, down, exec, pypr layout_center next2
```

> [!note]
> **Added in version 1.8.0**

# Command

- `layout_center [command]` where *[command]* can be:
  - next
  - prev
  - toggle

# Configuration

## `margin` (optional)

margin (in pixels) used when placing the center window, calculated from the border of the screen.

## `offset` (optional)

offset in pixels applied after the window position & size are computed regarding *margin*.

## `vertical` (optional)

If the *layout_center* isn't active, trigger focus "up" or "down" instead of "left" and "right".

