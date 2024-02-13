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

# lists are possible on the right part of the assignment:
"XYZ brand".leftOf = ["Sony", "BenQ"]

#You can also use "port" names such as *HDMI-A-1*, *DP-1*, etc... wrapping them in *()*:
" (HDMI-A-1)".bottom_of = "(eDP-1)"
# or, for a list:
"(HDMI-A-1)".bottom_of = ["(eDP-1)", "(DP-1)"]
# things can be mixed
Sony.bottom_of = ["(eDP-1)", "BenQ"]

# Thanks to TOML format, complex configurations can use separate "sections" for clarity, eg:

[monitors.placement."My monitor brand"]
leftOf = "(eDP-1)"

[monitors.placement."My other screen"]
topOf = "(eDP-1)"
```




Try to keep the rules as simple as possible, but relatively complex scenarios are supported.

> [!note]
> Check [wlr layout UI](https://github.com/fdev31/wlr-layout-ui) which is a nice complement to configure your monitor settings.

# Commands

## `relayout`

Collect every rule and recompute the monitors layout.

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

Default to `false`.
When set to `true`, performs a full "relayout" when a monitor is plugged instead of trying to minimize changes to apply.
