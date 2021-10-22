from time import sleep_us
from machine import Pin


class ShiftRegister7648:

    clock_cycle = 1  # microseconds

    def __init__(self, serial, clock, clear):
        self._serial = Pin(serial, Pin.OUT)
        self._clock = Pin(clock, Pin.OUT)
        self._clear = Pin(clear, Pin.OUT)

        self._serial.off()
        self._clock.off()
        self._clear.on()

    def clear(self):
        self._clear.off()
        sleep_us(self.clock_cycle)
        self._clear.on()
        sleep_us(self.clock_cycle)

    def write_bit(self, bit):
        if bit:
            self._serial.on()
        else:
            self._serial.off()
        self._clock.on()
        sleep_us(self.clock_cycle)
        self._clock.off()
        sleep_us(self.clock_cycle)

    def write_byte(self, byte):
        for i in range(8):
            self.write_bit(byte & (1 << i))
