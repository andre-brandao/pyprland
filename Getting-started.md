❯ git diff
diff --git a/pyprland/plugins/scratchpads.py b/pyprland/plugins/scratchpads.py
index 9118f18..36aaa34 100644
--- a/pyprland/plugins/scratchpads.py
+++ b/pyprland/plugins/scratchpads.py
@@ -152,7 +152,7 @@ class Extension(Plugin):
 
         # not known yet
         for name in new_scratches:
-            if not self.scratches[name].conf.get("lazy", False):
+            if not self.scratches[name].conf.get("lazy", True):
                 self.start_scratch_command(name)
 
     def start_scratch_command(self, name: str) -> None:
❯ git commit .
❯ tig
❯ git diff
diff --git a/pyprland/plugins/scratchpads.py b/pyprland/plugins/scratchpads.py
index 9118f18..36aaa34 100644
--- a/pyprland/plugins/scratchpads.py
+++ b/pyprland/plugins/scratchpads.py
@@ -152,7 +152,7 @@ class Extension(Plugin):
 
         # not known yet
         for name in new_scratches:
      "scratchpads",
      "monitors",
      "workspaces_follow_focus"
    ]
  },
  "scratchpads": {
    "term": {
      "command": "kitty --class kitty-dropterm",
      "animation": "fromTop",
      "unfocus": "hide"
    },
    "volume": {
      "command": "pavucontrol",
      "unfocus": "hide",
      "animation": "fromRight"
    }
  },
  "monitors": {
    "placement": {
      "BenQ PJ": {
        "topOf": "eDP-1"
      }
    }
    "unknown": "wlrlui"
  }
}
```
