import random

import can
from bmp import *


class Module:
    __slots__ = ("id", "solved", "manual", "info")

    def __init__(self, id_):
        self.id = id_
        self.solved = False
        self.manual = None
        self.info = None


class ControllerBMP(AsyncBMP):

    def __init__(self):
        super().__init__(MASTER)
        self.data_handler = {}

    def _on_data(self, sender, msg_type, data):
        if msg_type in self.data_handler:
            asyncio.create_task(self.data_handler[msg_type](sender, data))


class Controller:

    SERIAL_NO_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

    def __init__(self):
        self.bmp = ControllerBMP()

        self.bmp.request_handler[MSG_REGISTER] = self.add_module
        self.bmp.data_handler[MSG_RTFM] = self.set_manual
        self.bmp.data_handler[MSG_MODULE_INFO] = self.set_module_info
        self.bmp.request_handler[MSG_STRIKE] = self.add_strike
        self.bmp.request_handler[MSG_DETONATE] = self.detonate
        self.bmp.request_handler[MSG_MARK_SOLVED] = self.mark_solved
        self.bmp.request_handler[MSG_MARK_REACTIVATED] = self.mark_reactivated
        self.bmp.data_handler[MSG_CHANGE_TIMER] = self.change_timer
        self.bmp.request_handler[MSG_CHANGE_SERIAL_NO] = self.change_serial_no
        self.bmp.request_handler[MSG_TIMER] = self.send_timer
        self.bmp.request_handler[MSG_SERIAL_NO] = self.send_serial_no
        self.bmp.request_handler[MSG_STRIKES] = self.send_strikes
        self.bmp.request_handler[MSG_MAX_STRIKES] = self.send_max_strikes
        self.bmp.request_handler[MSG_MODULE_COUNT] = self.send_module_count
        self.bmp.request_handler[MSG_ACTIVE_MODULE_COUNT] = self.send_active_module_count
        self.bmp.request_handler[MSG_DIFFICULTY] = self.send_difficulty
        self.bmp.request_handler[MSG_LABELS] = self.send_labels

        self.modules = []
        self.max_strikes = 3
        self.strikes = 0
        self.timer = 1000000
        self.serial_no = " Wololo "
        self.difficulty = 0
        self.labels = {
            "FOO": True,
            "BAR": False
        }

    async def start(self):
        for i in range(1, 16):
            self.bmp.request(i, MSG_INIT)

        for i in range(1000):
            await asyncio.sleep_ms(1)

        for m in self.modules:
            self.bmp.request(m.id, MSG_RTFM)
            self.bmp.request(m.id, MSG_MODULE_INFO)

        while True:
            for m in self.modules:
                if m.manual is None or m.info is None:
                    break
            else:
                break
            await asyncio.sleep_ms(1)

        for m in self.modules:
            self.bmp.request(m.id, MSG_START)

        while True:
            await asyncio.sleep_ms(1)

    async def add_module(self, module):
        self.modules.append(Module(module))

    async def set_module_info(self, module, info):
        self.modules[module].info = info

    async def set_manual(self, module, manual):
        self.modules[module].manual = manual

    async def add_strike(self, _):
        self.strikes += 1
        if self.strikes >= self.max_strikes:
            await self.detonate(_)

    async def detonate(self, _):
        for m in self.modules:
            self.bmp.request(m.id, MSG_EXPLODED)

    async def mark_solved(self, module):
        self.modules[module].solved = True

    async def mark_reactivated(self, module):
        self.modules[module].solved = False

    async def change_serial_no(self, _):
        self.serial_no = "".join(random.choice(self.SERIAL_NO_ALPHABET) for _ in range(8))

    async def change_timer(self, _, data):
        delta = struct.unpack(">h", data)[0]
        self.timer += delta

    async def send_timer(self, module):
        self.bmp.send(module, MSG_TIMER, struct.pack(">I", self.timer))

    async def send_serial_no(self, module):
        self.bmp.send(module, MSG_SERIAL_NO, self.serial_no)

    async def send_strikes(self, module):
        self.bmp.send(module, MSG_STRIKES, struct.pack(">B", self.timer))

    async def send_max_strikes(self, module):
        self.bmp.send(module, MSG_MAX_STRIKES, struct.pack(">B", self.timer))

    async def send_module_count(self, module):
        self.bmp.send(module, MSG_MODULE_COUNT, struct.pack(">B", len(self.modules)))

    async def send_active_module_count(self, module):
        self.bmp.send(module, MSG_ACTIVE_MODULE_COUNT,
                      struct.pack(">B", len([None for module in self.modules if module.solved])))

    async def send_difficulty(self, module):
        self.bmp.send(module, MSG_DIFFICULTY, struct.pack(">B", self.difficulty))

    async def send_labels(self, module):
        data = ""
        for key, value in self.labels:
            data += "\x01" if value else "\x00"
            data += key
        self.bmp.send(module, MSG_LABELS, data)

try:
    can.stop()
except can.EspStateError:
    pass

can.start(1000)

asyncio.run(Controller().start())
