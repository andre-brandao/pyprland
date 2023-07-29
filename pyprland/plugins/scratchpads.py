" Scratchpads addon "
import os
import asyncio
import subprocess
from typing import Any

from ..ipc import (
    hyprctl,
    hyprctlJSON,
    get_focused_monitor_props,
)

from .interface import Plugin

DEFAULT_MARGIN = 60


async def get_client_props_by_address(addr: str):
    "Returns client properties given its address"
    for client in await hyprctlJSON("clients"):
        assert isinstance(client, dict)
        if client.get("address") == addr:
            return client


class Animations:
    "Animation store"

    @classmethod
    async def fromtop(cls, monitor, client, client_uid, margin):
        "Slide from/to top"
        scale = float(monitor["scale"])
        mon_x = monitor["x"]
        mon_y = monitor["y"]
        mon_width = int(monitor["width"] / scale)

        client_width = client["size"][0]
        margin_x = int((mon_width - client_width) / 2) + mon_x

        await hyprctl(f"movewindowpixel exact {margin_x} {mon_y + margin},{client_uid}")

    @classmethod
    async def frombottom(cls, monitor, client, client_uid, margin):
        "Slide from/to bottom"
        scale = float(monitor["scale"])
        mon_x = monitor["x"]
        mon_y = monitor["y"]
        mon_width = int(monitor["width"] / scale)
        mon_height = int(monitor["height"] / scale)

        client_width = client["size"][0]
        client_height = client["size"][1]
        margin_x = int((mon_width - client_width) / 2) + mon_x
        await hyprctl(
            f"movewindowpixel exact {margin_x} {mon_y + mon_height - client_height - margin},{client_uid}"
        )

    @classmethod
    async def fromleft(cls, monitor, client, client_uid, margin):
        "Slide from/to left"
        scale = float(monitor["scale"])
        mon_x = monitor["x"]
        mon_y = monitor["y"]
        mon_height = int(monitor["height"] / scale)

        client_height = client["size"][1]
        margin_y = int((mon_height - client_height) / 2) + mon_y

        await hyprctl(f"movewindowpixel exact {margin + mon_x} {margin_y},{client_uid}")

    @classmethod
    async def fromright(cls, monitor, client, client_uid, margin):
        "Slide from/to right"
        scale = float(monitor["scale"])
        mon_x = monitor["x"]
        mon_y = monitor["y"]
        mon_width = int(monitor["width"] / scale)
        mon_height = int(monitor["height"] / scale)

        client_width = client["size"][0]
        client_height = client["size"][1]
        margin_y = int((mon_height - client_height) / 2) + mon_y
        await hyprctl(
            f"movewindowpixel exact {mon_width - client_width - margin + mon_x } {margin_y},{client_uid}"
        )


class Scratch:
    "A scratchpad state including configuration & client state"

    def __init__(self, uid, opts):
        self.uid = uid
        self.pid = 0
        self.conf = opts
        self.visible = False
        self.just_created = True
        self.client_info = {}

    def isAlive(self) -> bool:
        "is the process running ?"
        path = f"/proc/{self.pid}"
        if os.path.exists(path):
            with open(os.path.join(path, "status"), "r", encoding="utf-8") as f:
                for line in f.readlines():
                    if line.startswith("State"):
                        state = line.split()[1]
                        return state in "RSDTt"  # not "Z (zombie)"or "X (dead)"
        return False

    def reset(self, pid: int) -> None:
        "clear the object"
        self.pid = pid
        self.visible = False
        self.just_created = True
        self.client_info = {}

    @property
    def address(self) -> str:
        "Returns the client address"
        return str(self.client_info.get("address", ""))[2:]

    async def updateClientInfo(self, clientInfo=None) -> None:
        "update the internal client info property, if not provided, refresh based on the current address"
        if clientInfo is None:
            clientInfo = await get_client_props_by_address("0x" + self.address)
        assert isinstance(clientInfo, dict)
        self.client_info.update(clientInfo)

    def __str__(self):
        return f"{self.uid} {self.address} : {self.client_info} / {self.conf}"


class Extension(Plugin):
    procs: dict[str, subprocess.Popen] = {}
    scratches: dict[str, Scratch] = {}
    transitioning_scratches: set[str] = set()
    _respawned_scratches: set[str] = set()
    scratches_by_address: dict[str, Scratch] = {}
    scratches_by_pid: dict[int, Scratch] = {}
    focused_window_tracking: dict[str, dict] = {}

    async def exit(self) -> None:
        "exit hook"

        async def die_in_piece(scratch: Scratch):
            proc = self.procs[scratch.uid]
            proc.terminate()
            for _ in range(10):
                if not scratch.isAlive():
                    break
                await asyncio.sleep(0.1)
            if scratch.isAlive():
                proc.kill()
            proc.wait()

        await asyncio.gather(
            *(die_in_piece(scratch) for scratch in self.scratches.values())
        )

    async def load_config(self, config) -> None:
        "config loader"
        config: dict[str, dict[str, Any]] = config["scratchpads"]
        scratches = {k: Scratch(k, v) for k, v in config.items()}

        new_scratches = set()

        for name in scratches:
            if name not in self.scratches:
                self.scratches[name] = scratches[name]
                new_scratches.add(name)
            else:
                self.scratches[name].conf = scratches[name].conf

        # not known yet
        for name in new_scratches:
            if not self.scratches[name].conf.get("lazy", False):
                await self.start_scratch_command(name)

    async def start_scratch_command(self, name: str) -> None:
        "spawns a given scratchpad's process"
        self._respawned_scratches.add(name)
        scratch = self.scratches[name]
        old_pid = self.procs[name].pid if name in self.procs else 0
        self.procs[name] = subprocess.Popen(
            scratch.conf["command"],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            shell=True,
        )
        pid = self.procs[name].pid
        self.scratches[name].reset(pid)
        self.scratches_by_pid[self.procs[name].pid] = scratch
        if old_pid and old_pid in self.scratches_by_pid:
            del self.scratches_by_pid[old_pid]

    # Events
    async def event_activewindowv2(self, addr) -> None:
        "active windows hook"
        addr = addr.strip()
        scratch = self.scratches_by_address.get(addr)
        if scratch:
            if scratch.just_created:
                await self.run_hide(scratch.uid, force=True)
                scratch.just_created = False
        else:
            for uid, scratch in self.scratches.items():
                if scratch.client_info and scratch.address != addr:
                    if (
                        scratch.visible
                        and scratch.conf.get("unfocus") == "hide"
                        and scratch.uid not in self.transitioning_scratches
                    ):
                        await self.run_hide(uid, autohide=True)

    async def event_openwindow(self, params) -> None:
        "open windows hook"
        addr, wrkspc, _kls, _title = params.split(",", 3)
        if wrkspc.startswith("special"):
            item = self.scratches_by_address.get(addr)
            if not item and self._respawned_scratches:
                # XXX: hack for windows which aren't related to the process
                class_lookup_hack = [
                    self.scratches[name]
                    for name in self._respawned_scratches
                    if self.scratches[name].conf.get("class")
                ]
                if class_lookup_hack:
                    self.log.debug("Lookup hack triggered")
                    for client in await hyprctlJSON("clients"):
                        assert isinstance(client, dict)
                        for pending_scratch in class_lookup_hack:
                            if pending_scratch.conf["class"] == client["class"]:
                                self.scratches_by_address[
                                    client["address"][2:]
                                ] = pending_scratch
                                self.log.debug("client class found: %s", client)
                                await pending_scratch.updateClientInfo(client)
                else:
                    await self.updateScratchInfo()
                item = self.scratches_by_address.get(addr)
            if item and item.just_created:
                self._respawned_scratches.discard(item.uid)
                await self.run_hide(item.uid, force=True)
                item.just_created = False

    async def run_toggle(self, uid: str) -> None:
        """<name> toggles visibility of scratchpad "name" """
        uid = uid.strip()
        item = self.scratches.get(uid)
        if not item:
            self.log.warning("%s is not configured", uid)
            return
        if item.visible:
            await self.run_hide(uid)
        else:
            await self.run_show(uid)

    async def updateScratchInfo(self, scratch: Scratch | None = None) -> None:
        """Update every scratchpads information if no `scratch` given,
        else update a specific scratchpad info"""
        if scratch is None:
            for client in await hyprctlJSON("clients"):
                assert isinstance(client, dict)
                scratch = self.scratches_by_address.get(client["address"][2:])
                if not scratch:
                    scratch = self.scratches_by_pid.get(client["pid"])
                    if scratch:
                        self.scratches_by_address[client["address"][2:]] = scratch
                if scratch:
                    await scratch.updateClientInfo(client)
        else:
            add_to_address_book = ("address" not in scratch.client_info) or (
                scratch.address not in self.scratches_by_address
            )
            await scratch.updateClientInfo()
            if add_to_address_book:
                self.scratches_by_address[scratch.client_info["address"][2:]] = scratch

    async def run_hide(self, uid: str, force=False, autohide=False) -> None:
        """<name> hides scratchpad "name" """
        uid = uid.strip()
        item = self.scratches.get(uid)
        if not item:
            self.log.warning("%s is not configured", uid)
            return
        if not item.visible and not force:
            self.log.warning("%s is already hidden", uid)
            return
        self.log.info("Hiding %s", uid)
        item.visible = False
        addr = "address:0x" + item.address
        animation_type: str = item.conf.get("animation", "").lower()
        if animation_type:
            offset = item.conf.get("offset")
            if offset is None:
                if "size" not in item.client_info:
                    await self.updateScratchInfo(item)

                offset = int(1.3 * item.client_info["size"][1])

            if animation_type == "fromtop":
                await hyprctl(f"movewindowpixel 0 -{offset},{addr}")
            elif animation_type == "frombottom":
                await hyprctl(f"movewindowpixel 0 {offset},{addr}")
            elif animation_type == "fromleft":
                await hyprctl(f"movewindowpixel -{offset} 0,{addr}")
            elif animation_type == "fromright":
                await hyprctl(f"movewindowpixel {offset} 0,{addr}")

            if uid in self.transitioning_scratches:
                return  # abort sequence
            await asyncio.sleep(0.2)  # await for animation to finish

        if uid not in self.transitioning_scratches:
            await hyprctl(f"movetoworkspacesilent special:scratch_{uid},{addr}")

        if (
            animation_type and uid in self.focused_window_tracking
        ):  # focus got lost when animating
            if not autohide and "address" in self.focused_window_tracking[uid]:
                await hyprctl(
                    f"focuswindow address:{self.focused_window_tracking[uid]['address']}"
                )
                del self.focused_window_tracking[uid]

    async def run_show(self, uid, force=False) -> None:
        """<name> shows scratchpad "name" """
        uid = uid.strip()
        item = self.scratches.get(uid)

        self.focused_window_tracking[uid] = await hyprctlJSON("activewindow")

        if not item:
            self.log.warning("%s is not configured", uid)
            return

        if item.visible and not force:
            self.log.warning("%s is already visible", uid)
            return

        self.log.info("Showing %s", uid)

        if not item.isAlive():
            self.log.info("%s is not running, restarting...", uid)
            if uid in self.procs:
                self.procs[uid].kill()
            if item.pid in self.scratches_by_pid:
                del self.scratches_by_pid[item.pid]
            if item.address in self.scratches_by_address:
                del self.scratches_by_address[item.address]
            await self.start_scratch_command(uid)
            while uid in self._respawned_scratches:
                await asyncio.sleep(0.05)

        item.visible = True
        monitor = await get_focused_monitor_props()
        assert monitor

        await self.updateScratchInfo(item)

        addr = "address:0x" + item.address

        animation_type = item.conf.get("animation", "").lower()

        wrkspc = monitor["activeWorkspace"]["id"]

        self.transitioning_scratches.add(uid)
        await hyprctl(f"moveworkspacetomonitor special:scratch_{uid} {monitor['name']}")
        await hyprctl(f"movetoworkspacesilent {wrkspc},{addr}")
        if animation_type:
            margin = item.conf.get("margin", DEFAULT_MARGIN)
            fn = getattr(Animations, animation_type)
            await fn(monitor, item.client_info, addr, margin)

        await hyprctl(f"focuswindow {addr}")
        await asyncio.sleep(0.2)  # ensure some time for events to propagate
        self.transitioning_scratches.discard(uid)
