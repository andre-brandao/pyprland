It's easy to write your own plugin by making a python package and then indicating it's name as the plugin name.

# Writing plugins

You can start enabling a plugin called "experimental" and add code to `plugins/experimental.py`.
A better way is to copy this as a starting point and make your own python module.
Plugins can be loaded with full python module path, eg: `"mymodule.pyprlandplugin"`, the loaded module must provide an `Extension` interface.

Check the `interface.py` file to know the base methods, also have a look at the other plugins for working examples.

To get more details when an error is occurring, `export DEBUG=1` in your shell before running.

## Creating a command

Just add a method called `run_<name of your command>`, eg with "togglezoom" command:

```python
async def init(self):
  self.zoomed = False

async def run_togglezoom(self, args):
  if self.zoomed:
    await hyprctl('misc:cursor_zoom_factor 1', 'keyword')
  else:
    await hyprctl('misc:cursor_zoom_factor 2', 'keyword')
  self.zoomed = not self.zoomed
```

## Reacting to an event

Similar as a command, implement some `event_<the event you are interested in>` method.

## Code safety

Pypr ensures only one `run_` or `event_` handler runs at a time, allowing the plugins code to stay simple and avoid the need for concurrency handling.
However, each plugin can run its handlers in parallel.
