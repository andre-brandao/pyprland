# `expose`

This plugin have two features:

The two commands are not really related, one allows the "expose" effect, showing every client window on the focused screen.
The other one allows you to have some kind of dynamic scratchpad, which can be used to minimize (and back) the windows.
They have in common the way they display the client windows to "restore" or "focus" to a specific one.

Sample `hyprland.conf`:

*toggle_minimized feature:*
```bash
bind = $mainMod SHIFT, U, togglespecialworkspace, minimized
bind = $mainMod , N, exec, pypr toggle_minimized
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

