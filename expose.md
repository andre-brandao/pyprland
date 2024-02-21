Implements the "expose" effect, showing every client window on the focused screen.

For a similar feature using a menu, try the [fetch_client_menu](fetch_client_menu) plugin (less intrusive).

Sample `hyprland.conf`:

```bash
bind = $mainMod, B, exec, pypr expose
```
`MOD+B` will bring every client to the focused workspace, pressed again it will go to this workspace.

> [!note]
> If you are looking for `toggle_minimized`, check the [[toggle_special]] plugin

# Commands

- `expose`: expose every client on the active workspace. If expose is already active, then restores everything and move to the focused window.

# Configuration


## `include_special` (optional)

default value is `false`

Also include windows in the special workspaces during the expose.

