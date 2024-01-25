Implements a "centered" workspace layout,
windows are tiled as usual but one, which is centered and "maximized".

On `toggle`, the active window is made floating and centered if the layout wasn't enabled, else reverts the floating status.

With `next` and `prev` you can cycle the active window, keeping the same layout type.

# Command

- `centerlayout [command]` where *[command]* can be:
  - next
  - prev
  - toggle

# Configuration

## `vertical` (optional)

If the *centerlayout* isn't active, trigger focus "up" or "down" instead of "left" and "right".

## `margin` (optional)

defaults to `100`

margin used when placing the center window, calculated from the border of the screen.

> [!note]
> **Added in version 1.8.0**
