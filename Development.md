It's easy to write your own plugin by making a python package and then indicating it's name as the plugin name.

# Writing plugins

Plugins can be loaded with full python module path, eg: `"mymodule.pyprlandplugin"`, the loaded module must provide an `Extension` class.

Check the `interface.py` file to know the base methods, also have a look at the example below.

To get more details when an error is occurring, `export DEBUG=1` in your shell before running `pypr`.

> [!note]
> To quickly get started, you can directly edit the `experimental` built-in plugin.
> In order to distribute it, make your own Python package or trigger a pull request.

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

# Example

You'll find a basic external plugin in the [examples](https://github.com/hyprland-community/pyprland/blob/main/examples/) folder.

It's a simple python package. To install it for development without a need to re-install it for testing, you can use `pip install -e .` in this folder.
It's ready to be published using `poetry publish`, don't forget to update the details in the `pyproject.toml` file.

## Usage

Ensure you added `pypr_examples.focus_counter` to your `plugins` list:

```toml
[pyprland]
plugins = [
  "pypr_examples.focus_counter"
]
```

Optionally you can customize one color:

```toml
["pypr_examples.focus_counter"]
color = "FFFF00"
```

It provides one command: `pypr dummy`.
Check the [source code](https://github.com/hyprland-community/pyprland/blob/main/examples/pypr_examples/focus_counter.py)

