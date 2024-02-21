Bring any window to the active workspace using a menu.

A bit like the [expose](expose) plugin but using a menu instead (less intrusive).

It brings the window to the current workspace, while [expose](expose) moves the currently focused screen to the application workspace.

This feature can also be provided by this plugin in the future, faster [if requested](https://github.com/hyprland-community/pyprland/issues/new?assignees=fdev31&labels=feature&projects=&template=feature_request.md&title=%5BFEAT%5D+Description+of+the+feature)

Sample `hyprland.conf`:

> [!note]
> Added in 1.10

# Commands

- `fetch_client_menu`: display the menu allowing selection of the client to show

# Configuration

All the [menu](_menu) configuration items are also available.

## `separator` (optional)

default value is `"|"`

Changes the character (or string) used to separate a menu entry from its entry number.

