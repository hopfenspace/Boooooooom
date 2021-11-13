try:
    import uasyncio as asyncio
except ImportError:
    import asyncio

import bmp
import can


class Module:

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
            # micropython has only one event loop so new_event_loop just resets it
            # run_forever runs until a task (probably a reset message from the master) calls stop on it
            # once stopped the infinite while loop resets the event_loop and restart it again
            loop.create_task(_loop())
            loop.run_forever()
            loop = asyncio.new_event_loop()
            loop.create_task(self.on_init(bmp.MASTER))


class DebugModule(Module):
    async def on_start(self, _):
        print("Got START")

    async def on_rtfm(self, requester):
        print("Got RTFM")
        self.bmp.send(requester, bmp.MSG_MODULE_INFO, "DEBUG")

    async def on_module_info(self, requester):
        print("Got MODULE_INFO")
        self.bmp.send(requester, bmp.MSG_MODULE_INFO, "DEBUG")
