Implements the "expose" effect, showing every client window on the focused screen.

Sample `hyprland.conf`:

```bash
bind = $mainMod, B, exec, pypr expose
```
`MOD+B` will bring every client to the focused workspace, pressed again it will go to this workspace.

# Commands

- `expose`: expose every client on the active workspace. If expose is already active, then restores everything and move to the focused window.

# Configuration


## `include_special` (optional)

defaults to `false`

Also include windows in the special workspaces during the expose.

