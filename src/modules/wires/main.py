from machine import Pin

import bmp
from module import Module


class WireModule(Module):

    def __init__(self, address, pins):
        super().__init__(address)
        # const
        self.potential_pins = [Pin(p, Pin.IN) for p in pins]

        # round based
        self.manual = ""
        self.active_pins = []
        self.wires_to_unplug = -1

    async def on_init(self, _):
        self.active_pins = []
        for pin in self.potential_pins:
            # Clear potential old interrupt
            pin.irq(None, trigger=Pin.IRQ_FALLING)

            # Probe which pin has a wire plugged in
            if pin.value():
                self.active_pins.append(pin)

        self.manual = "Unplug all but the first wire"
        self.wires_to_unplug = len(self.active_pins) - 1

    async def on_start(self, _):
        for i, pin in enumerate(self.active_pins):
            # Set new interrupt
            pin.irq(lambda _: self.on_unplugged(i), trigger=Pin.IRQ_FALLING)

    def on_unplugged(self, index):
        if index == 0:
            self.bmp.strike()
        else:
            self.wires_to_unplug -= 1
            if self.wires_to_unplug == 0:
                self.bmp.mark_solved()

    async def on_rtfm(self, _):
        await self.bmp.send(bmp.MASTER, bmp.MSG_RTFM, self.manual)

    async def on_module_info(self, requester):
        await self.bmp.send(requester, bmp.MSG_MODULE_INFO, "")


WireModule(15).run()
