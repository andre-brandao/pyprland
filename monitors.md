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

# lists are allowed on the right part of the assignment:
# "XYZ brand".leftOf = ["Sony", "BenQ"]
# Character case is ignored, "_" can be added
# Sony.Top_Of = ["BenQ"]
# Since monitor's description, you can use "(name)":
# "(HDMI-A-1)".leftof = "(eDP-1)"
```

You can also use "port" names such as *HDMI-A-1*, *DP-1*, etc... wrapping them in *()*:
```toml
"(HDMI-A-1)".bottom_of = ["(eDP-1)"]
```

> [!note]
> Check [wlr layout UI](https://github.com/fdev31/wlr-layout-ui) which is a nice complement to configure your monitor settings.

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

## `startup_relayout` (optional)

Default to `ŧrue`.
When set to `false`, do not initialize the monitor layout on startup or when configuration is reloaded.

## `full_relayout` (optional)

Default to `false`.
When set to `true`, performs a full "relayout" when a monitor is plugged instead of trying to minimize changes to apply.

# Known limitations

`relayout` isn't reliable with more than 2 monitors
