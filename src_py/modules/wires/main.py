from machine import Pin
import uasyncio

import bmp
from module import Module


class WireModule(Module):

    def __init__(self, address, pins):
        super().__init__(address)
        # const
        self.potential_pins = [Pin(p, Pin.IN, pull=Pin.PULL_DOWN) for p in pins]

        # round based
        self.manual = ""
        self.active_pins = []
        self.unplugged_pins = []
        self.is_running = uasyncio.Event()

    async def on_init(self, _):
        await super().on_init(_)

        def create_irq(index):
            def handler(_):
                uasyncio.create_task(self.on_unplugged(index))
            return handler

        self.active_pins = []
        self.unplugged_pins = []
        self.is_running.clear()
        for pin in self.potential_pins:
            # Probe which pin has a wire plugged in
            if pin.value():
                pin.irq(create_irq(len(self.active_pins)), trigger=Pin.IRQ_FALLING)
                self.active_pins.append(pin)
                self.unplugged_pins.append(False)
            else:
                pin.irq(None, trigger=Pin.IRQ_FALLING)

        self.manual = "Unplug all but the first wire"

    async def on_start(self, _):
        self.is_running.set()

    async def on_unplugged(self, index):
        # Delay all events until game start
        await self.is_running.wait()

        if not self.unplugged_pins[index]:
            self.unplugged_pins[index] = True
            if index == 0:
                self.bmp.strike()
            elif all(self.unplugged_pins[1:]):
                self.bmp.mark_solved()

    async def on_rtfm(self, _):
        self.bmp.send(bmp.MASTER, bmp.MSG_RTFM, self.manual)

    async def on_module_info(self, requester):
        self.bmp.send(requester, bmp.MSG_MODULE_INFO, "")


WireModule(15, [25, 26, 27]).run()
