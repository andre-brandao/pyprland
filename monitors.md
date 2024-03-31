> [!note]
> First version of the plugin is still available under the name `monitors_v0`

Allows relative placement of monitors depending on the model ("description" returned by `hyprctl monitors`).
Useful if you have multiple monitors connected to a video signal switch or using a laptop and plugging monitors having different relative positions.

Requires `wlr-randr`.

Syntax:

```toml
[monitors]
unknown = "program to run"

[monitors.placement]
"description match".placement = "other description match"
```

Example to set a Sony monitor on top of the BenQ monitor:
```toml
[monitors.placement]
Sony.topOf = "BenQ"

# Character case is ignored, "_" can be added
Sony.Top_Of = ["BenQ"]

# Thanks to TOML format, complex configurations can use separate "sections" for clarity, eg:

[monitors.placement."My monitor brand"]
# You can also use "port" names such as *HDMI-A-1*, *DP-1*, etc... 
leftOf = "eDP-1"

# lists are possible on the right part of the assignment:
rightOf = ["Sony", "BenQ"]
```

Try to keep the rules as simple as possible, but relatively complex scenarios are supported.

> [!note]
> Check [wlr layout UI](https://github.com/fdev31/wlr-layout-ui) which is a nice complement to configure your monitor settings.

# Commands

- `relayout` : Apply the configuration and update the layout

# Configuration

## `placement`

Supported placements are:

- leftOf
- topOf
- rightOf
- bottomOf
- \<one of the above>(center|middle|end)Of *

> \* If you don't like the screen to align on the start of the given border, you can use `center` (or `middle`) to center it or `end` to stick it to the opposite border.
> Eg: "topCenterOf", "leftEndOf", etc...

You can separate the terms with "_" to improve the readability, as in "top_center_of".

## `startup_relayout` (optional)

Default to `ŧrue`.

When set to `false`, do not initialize the monitor layout on startup or when configuration is reloaded.

## `full_relayout` (optional)

Default to `true`.

When set to `false`, use the former incremental layout, trying to minimize changes.

> [!important]
>
> This command is planned to be deprecated/removed. If you need it, report some [feedback](https://github.com/hyprland-community/pyprland/issues/new/choose)

## `new_monitor_delay` (optional)

By default, the layout computation happens one second after the event is received to let time for things to settle.

You can change this value using this option.

