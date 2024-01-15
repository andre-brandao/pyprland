# General

In case of trouble running a `pypr` command:
- kill the existing pypr if any
- run from the terminal adding `--debug /dev/null` to the arguments to get more information

If the client says it can't connect, then there is a high chance pypr daemon didn't start, check if it's running using `ps axuw |grep pypr`. You can try to run it from a terminal with the same technique: `pypr --debug /dev/null` and see if any error occurs.

In case you figure it's broken only when running from `hyprland.conf` using `exec-once`:

Run it using the following command and check the log file:

```sh
pypr --debug /dev/null > /tmp/pypr_launch_log.txt 2>&1
```

 
# Scratchpads

> *TLDR*
>
> If a process isn't behaving properly, try `process_tracking = false` and/or `class_match = true`.
> Check https://github.com/hyprland-community/pyprland/wiki/Plugins#class_match-optional for more details.

## Disable PID tracking (eg: `emacsclient`)

Some apps may open the graphical client window in a "complicated" way, to work around this, it is possible to disable the process PID matching algorithm and simply rely on window's class.
The `class_match` attribute can be used to achieve this, eg. for emacsclient:
```toml
[scratchpads.emacs]
command = "/usr/local/bin/emacsStart.sh"
class = "Emacs"
class_match = true
```

## Disable process management

Progressive web apps will share a single process for every window.
On top of requiring the class based window tracking (using `class_match`), the process can not be managed the same way as usual apps and the correlation between the process and the client window isn't as straightforward and can lead to false matches in extreme cases.

However, this is possible to run those apps in a scratchpad by setting `process_tracking = false`.

Check [the `process_tracking` option](https://github.com/hyprland-community/pyprland/wiki/Plugins#process_tracking-optional---discouraged)

## Pypr freezes for some time when it fails showing a scratchpad

This may happen due to some application's behavior, for instance `pavucontrol` which can freeze on startup without being able to create a window if another instance is running.
In that case pypr will wait for a window which will never be available before giving up after a few seconds.
For `pavucontrol` the solution is simple: just kill it (`pkill pavucontrol`) and try to show the scratchpad that will launch it again!
