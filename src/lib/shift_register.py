import time
import uasyncio

from machine import Pin


def _toggle(pin):
    if pin.value():
        pin.off()
    else:
        pin.on()


class ShiftRegister:

    clock_cycle = 1  # microseconds

    def _pulse(self, pin):
        _toggle(pin)
        time.sleep_us(self.clock_cycle)
        _toggle(pin)
        time.sleep_us(self.clock_cycle)

    def write_bit(self, bit):
        raise NotImplementedError

    def write_int(self, integer, *, bits=8, most_significant_first=True):
        if most_significant_first:
            order = range(bits-1, -1, -1)
        else:
            order = range(bits)
        for bit in order:
            self.write_bit(integer & (1 << bit))


class AsyncShiftRegister:

    clock_cycle = 1  # microseconds

    async def _pulse(self, pin):
        _toggle(pin)
        await uasyncio.sleep_us(self.clock_cycle)
        _toggle(pin)
        await uasyncio.sleep_us(self.clock_cycle)

    async def write_bit(self, bit):
        raise NotImplementedError

    async def write_int(self, integer, *, bits=8, most_significant_first=True):
        if most_significant_first:
            order = range(bits-1, -1, -1)
        else:
            order = range(bits)
        for bit in order:
            await self.write_bit(integer & (1 << bit))


class ShiftRegisterSNx4HC595(ShiftRegister):

    __slots__ = ("_serial", "_storage_clock", "_shift_clock", "_clear")

    def __init__(self, *, ser, srclk, rclk, srclr):
        self._serial = Pin(ser, Pin.OUT)
        self._storage_clock = Pin(rclk, Pin.OUT, value=0)
        self._shift_clock = Pin(srclk, Pin.OUT, value=0)
        self._clear = Pin(srclr, Pin.OUT, value=1)

    def clear(self):
        self._pulse(self._clear)
        self.push()

    def push(self):
        self._pulse(self._storage_clock)

    def write_bit(self, bit):
        if bit:
            self._serial.on()
        else:
            self._serial.off()
        self._pulse(self._shift_clock)

    def write_int(self, integer, *, bits=8, most_significant_first=True, push=True):
        super().write_int(integer, bits=bits, most_significant_first=most_significant_first)
        if push:
            self.push()


class AsyncShiftRegisterSNx4HC595(AsyncShiftRegister):

    __slots__ = ("_serial", "_storage_clock", "_shift_clock", "_clear")

    def __init__(self, *, ser, srclk, rclk, srclr):
        self._serial = Pin(ser, Pin.OUT)
        self._storage_clock = Pin(rclk, Pin.OUT, value=0)
        self._shift_clock = Pin(srclk, Pin.OUT, value=0)
        self._clear = Pin(srclr, Pin.OUT, value=1)

    async def clear(self):
        await self._pulse(self._clear)
        await self.push()

    async def push(self):
        await self._pulse(self._storage_clock)

    async def write_bit(self, bit):
        if bit:
            self._serial.on()
        else:
            self._serial.off()
        await self._pulse(self._shift_clock)

    async def write_int(self, integer, *, bits=8, most_significant_first=True, push=True):
        await super().write_int(integer, bits=bits, most_significant_first=most_significant_first)
        if push:
            await self.push()
