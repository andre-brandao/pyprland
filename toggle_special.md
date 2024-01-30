Allows moving the focused window to a special workspace and back. Must be complemented with the `togglespecialworkspace` Hyprland's command for a better user experience.
If not specified, uses the "minimized" special workspace.

Sample `hyprland.conf`:

```bash
bind = $mainMod SHIFT, N, togglespecialworkspace, minimized
bind = $mainMod, N, exec, pypr toggle_special
```

No other configuration needed, here `MOD+SHIFT+U` will show every "minimized" clients, while `MOD+N` will (un)minimize the focused client.

# Commands

- `toggle_special [name]`: moves the focused window to the special workspace "name", or move it back to the active workspace.
    If none set, a special workspace called "minimized" will be used.
    To toggle the state back to a normal workspace, you'll need to `hyprctl dispatch togglespecialworkspace minimized` (if you didn't set a name, since "minimized" is the default special workspace that will be used).
    It can also be achieved with a keybinding: `bind = $mainMod SHIFT, N, togglespecialworkspace, minimized` in `hyprland.conf`


Example usage in `hyprland.conf`:

```
bind = $mainMod, N, exec, pypr toggle_special
 ```
