try:
    import uasyncio as asyncio
except ImportError:
    import asyncio

import bmp
import can


class Module:
    """
    This can be used as a base class for any module.

    It registers its `on_<message>` methods as bmp request handlers
    and provides a simple run method handling weird uasyncio stuff.

    Usage:
    - Extend this class and implement at least the `on_start`, `on_rtfm` and `on_module_info` methods.
    - Create one object of your class and call `run` on it.

    Notes:
    - the constructor should only assign attributes which stay constant
    - any value which might change during play, should be set in the `on_init` method
      (don't forget to add an `await super().on_init(_)`!)
    """

    def __init__(self, address):
        self.is_solved = False

        #  Stop can
        try:
            can.stop()
        except RuntimeError:
            pass  # can wasn't running

        # Setup bmp connection
        self.bmp = bmp.AsyncBMP(address)
        # self.bmp.request_handler[bmp.MSG_RESET] = self.on_reset
        self.bmp.request_handler[bmp.MSG_INIT] = self._on_init
        self.bmp.request_handler[bmp.MSG_START] = self.on_start
        self.bmp.request_handler[bmp.MSG_DEFUSED] = self.on_defused
        self.bmp.request_handler[bmp.MSG_EXPLODED] = self.on_exploded
        self.bmp.request_handler[bmp.MSG_RTFM] = self.on_rtfm
        self.bmp.request_handler[bmp.MSG_VERSION] = self.on_version
        self.bmp.request_handler[bmp.MSG_MODULE_INFO] = self.on_module_info
        self.bmp.request_handler[bmp.MSG_BLACKOUT] = self.on_blackout
        self.bmp.request_handler[bmp.MSG_IS_SOLVED] = self.on_is_solved

        # Start can
        can.start(1000)

    async def _on_init(self, _):
        # Stop event loop and wait for new one to call `on_init`
        # See `run` for more details
        asyncio.get_event_loop().stop()

    async def on_init(self, _):
        self.is_solved = False
        self.bmp.register()

    async def on_start(self, _):
        raise NotImplementedError

    async def on_defused(self, _):
        pass

    async def on_exploded(self, _):
        pass

    async def on_rtfm(self, _):
        raise NotImplementedError

    async def on_version(self, requester):
        await self.bmp.send(requester, bmp.MSG_VERSION, "1")

    async def on_module_info(self, _):
        raise NotImplementedError

    async def on_blackout(self, _):
        pass

    async def on_is_solved(self, requester):
        await self.bmp.send(requester, bmp.MSG_IS_SOLVED, "\x01" if self.is_solved else "\x00")

    def run(self):
        # Keep loop busy and stop him from stopping
        async def _loop():
            while True:
                await asyncio.sleep(1)

        # Reset event loop
        loop = asyncio.new_event_loop()
        while True:
            loop.create_task(_loop())  # Keep loop busy and stop him from stopping
            loop.run_forever()  # Run until bmp receives a MSG_INIT (see `_on_init`)
            loop = asyncio.new_event_loop()  # Reset event loop to clear old tasks
            loop.create_task(self.on_init(bmp.MASTER))  # Schedule the module's actual `on_init`
            # Reenter `while True` to start event_loop and run `on_init`
        # This whole setup's purpose is to reset/ clear the event loop on a MSG_INIT


class DebugModule(Module):
    async def on_start(self, _):
        print("Got START")

    async def on_rtfm(self, requester):
        print("Got RTFM")
        self.bmp.send(requester, bmp.MSG_MODULE_INFO, "DEBUG")

    async def on_module_info(self, requester):
        print("Got MODULE_INFO")
        self.bmp.send(requester, bmp.MSG_MODULE_INFO, "DEBUG")
