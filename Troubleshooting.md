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

## Disable PID tracking (eg: `emacsclient`)

Some apps may open the graphical client window in a "complicated" way, to work around this, it is possible to disable the process PID matching algorithm and simply rely on window's class.
The `class` attribute can be used to achieve this, eg. for emacsclient:
```json
"emacs": {
        "command": "/usr/local/bin/emacsStart.sh",
        "unfocus": "hide",
        "class": "Emacs"
      }
```