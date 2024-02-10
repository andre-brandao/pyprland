Bring any window to the active workspace using a menu.

A bit like the *expose* plugin but using a menu instead (less intrusive).

Sample `hyprland.conf`:

> [!note]
> Added in 1.10

# Commands

- `fetch_client_menu`: display the menu allowing selection of the client to show

# Configuration


## `separator` (optional)
S
default value is `"|"`

Changes the character (or string) used to separate a menu entry from its entry number.


## `engine` (optional)

Not set by default, will autodetect the available menu engine.

Supported engines:

- tofi
- rofi
- wofi
- bemenu
- dmenu

> [!note]
> If your menu system isn't supported, you can open a [feature request](https://github.com/hyprland-community/pyprland/issues/new?assignees=fdev31&labels=bug&projects=&template=feature_request.md&title=%5BFEAT%5D+Description+of+the+feature)
>
> In case the engine isn't recognized, `engine` + `parameters` configuration options will be used to start the process, it requires a dmenu-like behavior.

## `parameters` (optional)

Extra parameters added to the engine command, the default value is specific to each engine.

