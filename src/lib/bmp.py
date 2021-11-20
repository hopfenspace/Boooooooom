from micropython import const
try:
    import uasyncio as asyncio
except ImportError:
    import asyncio
import struct

import can


MASTER = const(0x00)

MSG_RESET = const(0x00)  # request_handler required
MSG_INIT = const(0x01)  # request_handler required
MSG_START = const(0x02)  # request_handler required
MSG_DEFUSED = const(0x03)  # request_handler required
MSG_EXPLODED = const(0x04)  # request_handler required
MSG_RTFM = const(0x05)  # request_handler required
MSG_VERSION = const(0x06)  # request_handler required
MSG_MODULE_INFO = const(0x07)  # request_handler required
MSG_REGISTER = const(0x08)
MSG_STRIKE = const(0x09)
MSG_DETONATE = const(0x0a)
MSG_MARK_SOLVED = const(0x0b)
MSG_MARK_REACTIVATED = const(0x0c)
MSG_CHANGE_TIMER = const(0x0d)
MSG_CHANGE_SERIAL_NO = const(0x0e)
MSG_TIMER = const(0x0f)
MSG_SERIAL_NO = const(0x10)
MSG_STRIKES = const(0x11)
MSG_MAX_STRIKES = const(0x12)
MSG_MODULE_COUNT = const(0x13)
MSG_ACTIVE_MODULE_COUNT = const(0x14)
MSG_DIFFICULTY = const(0x15)
MSG_LABELS = const(0x16)
MSG_BLACKOUT = const(0x17)  # request_handler required
MSG_IS_SOLVED = const(0x18)  # request_handler required
MSG_SEED = const(0x19)

# List of difficulty names (use the numeric difficulty as index)
DIFFICULTY_NAMES = [
    "IMMORTAL",
    "TRAINING",
    "EASY",
    "NORMAL",
    "HARD",
    "EXPERT",
    "PREPARE_2_DIE"
]
DIF_IMMORTAL = const(0)
DIF_TRAINING = const(1)
DIF_EASY = const(2)
DIF_NORMAL = const(3)
DIF_HARD = const(4)
DIF_EXPERT = const(5)
DIF_PREPARE_2_DIE = const(6)


def _ascii(data):
    return data


def _uint8(data):
    return struct.unpack(">B", data)[0]


def _uint32(data):
    return struct.unpack(">I", data)[0]


def _int32(data):
    return struct.unpack(">i", data)[0]


def _labels(data):
    labels = {}
    for i in range(len(data)//4):
        labels[data[4*i+1:4*(i+1)]] = data[4*i] != "\x00"
    return labels


_converter = {
    MSG_TIMER: _uint32,
    MSG_SERIAL_NO: _ascii,
    MSG_STRIKES: _uint8,
    MSG_MAX_STRIKES: _uint8,
    MSG_MODULE_COUNT: _uint8,
    MSG_ACTIVE_MODULE_COUNT: _uint8,
    MSG_DIFFICULTY: _uint8,
    MSG_LABELS: _labels,
    MSG_SEED: _uint32,
}


def _format_id(sender, recipient, msg_type, eot=1):
    return ((((((sender << 4) + recipient) << 8) + msg_type) << 1) + eot) << 12


def _parse_id(id_):
    id_ = id_ >> 12
    eot = id_ & 1
    id_ = id_ >> 1
    msg_type = id_ & 255
    id_ = id_ >> 8
    recipient = id_ & 15
    id_ = id_ >> 4
    sender = id_ & 15
    return sender, recipient, msg_type, eot


class _Pointer:
    """
    This class just holds a single mutable value: `data`

    It's purpose is to reduce lookups in the `AsyncBMP._requests` dict,
    by being a static pointer to the updating inner data.
    """
    __slots__ = ("data",)

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f"Pointer(data={repr(self.data)})"


# Singleton indicating a running request
_WAITING = object()


class AsyncBMP:

    def __init__(self, address):
        self.address = address

        self.request_handler = {}
        """function taking the sender address and returning nothing"""

        self._ongoing_data = {}
        """map from (sender, msg_type) to string"""

        self._requests = {}
        """Map from (msg_type, target) to _Pointers to the request's data or the _WAITING singleton"""
        self._lock = asyncio.Lock()
        """Lock to sync write access to the _requests dict"""

        can.on_receive(self._on_receive)

    def _on_receive(self, messages):
        for id_, ext, request, data_or_dlc in messages:
            sender, recipient, msg_type, eot = _parse_id(id_)
            if recipient == self.address:
                if request:
                    self._on_request(sender, msg_type)
                else:
                    if (sender, msg_type) in self._ongoing_data:
                        self._ongoing_data[(sender, msg_type)] += data_or_dlc
                    else:
                        self._ongoing_data[(sender, msg_type)] = data_or_dlc

                    if eot:
                        data = self._ongoing_data[(sender, msg_type)]
                        del self._ongoing_data[(sender, msg_type)]
                        self._on_data(sender, msg_type, data)

    def _on_request(self, requester, msg_type):
        if msg_type in self.request_handler:
            asyncio.create_task(self.request_handler[msg_type](requester))

    def _on_data(self, sender, msg_type, data):
        if (msg_type, sender) in self._requests:
            request: _Pointer = self._requests[(msg_type, sender)]
            if request.data is _WAITING:
                request.data = data

    def request(self, recipient, msg_type):
        # Just send the request over can
        can.transmit(_format_id(self.address, recipient, msg_type), True, True, 0)

    async def request_data(self, recipient, msg_type):
        requests: dict = self._requests  # Reduce lookups while holding the lock

        async with self._lock:
            try:
                # Get the current request
                request: _Pointer = requests[(msg_type, recipient)]
                # Check if the request has already finished
                new = request.data is not _WAITING
            except KeyError:
                # If there is no request yet, we have to create one
                new = True

            if new:
                # Create new request object
                request = _Pointer(_WAITING)
                requests[(msg_type, recipient)] = request

        if new:
            self.request(recipient, msg_type)

        while request.data is _WAITING:
            await asyncio.sleep_ms(1)

        if msg_type in _converter:
            return _converter[msg_type](request.data)
        else:
            return request.data

    def send(self, recipient, msg_type, data):
        packets = len(data) // 8
        if len(data) % 8 != 0:
            packets += 1
        for i in range(packets):
            eot = 1 if i == packets - 1 else 0
            can.transmit(_format_id(self.address, recipient, msg_type, eot), True, False, data[i * 8:])

    # Request action from master
    def register(self):
        self.request(MASTER, MSG_REGISTER)

    def strike(self):
        self.request(MASTER, MSG_STRIKE)

    def detonate(self):
        self.request(MASTER, MSG_DETONATE)

    def mark_solved(self):
        self.request(MASTER, MSG_MARK_SOLVED)

    def mark_reactived(self):
        self.request(MASTER, MSG_MARK_REACTIVATED)

    def change_timer(self, timedelta):
        self.send(MASTER, MSG_CHANGE_TIMER, timedelta.to_bytes(2, "big"))

    def change_serial_no(self):
        self.request(MASTER, MSG_CHANGE_SERIAL_NO)

    # Request data from master
    async def timer(self):
        return await self.request_data(MASTER, MSG_TIMER)

    async def serial_no(self):
        return await self.request_data(MASTER, MSG_SERIAL_NO)

    async def strikes(self):
        return await self.request_data(MASTER, MSG_STRIKES)

    async def max_strikes(self):
        return await self.request_data(MASTER, MSG_MAX_STRIKES)

    async def modules(self):
        return await self.request_data(MASTER, MSG_MODULE_COUNT)

    async def active_modules(self):
        return await self.request_data(MASTER, MSG_ACTIVE_MODULE_COUNT)

    async def difficulty(self):
        return await self.request_data(MASTER, MSG_DIFFICULTY)

    async def labels(self):
        return await self.request_data(MASTER, MSG_LABELS)

    async def seed(self):
        return await self.request_data(MASTER, MSG_SEED)

    # Request data from target
    async def version(self, target):
        return await self.request_data(target, MSG_VERSION)

    async def module_info(self, target):
        return await self.request_data(target, MSG_MODULE_INFO)

    async def is_solved(self, target):
        return await self.request_data(target, MSG_IS_SOLVED)


class SyncBMP(AsyncBMP):

    def _on_request(self, requester, msg_type):
        if msg_type in self.request_handler:
            self.request_handler[msg_type](requester)

    # Request data from master
    def timer(self):
        return asyncio.run(super().timer())

    def serial_no(self):
        return asyncio.run(super().serial_no())

    def strikes(self):
        return asyncio.run(super().strikes())

    def max_strikes(self):
        return asyncio.run(super().max_strikes())

    def modules(self):
        return asyncio.run(super().modules())

    def active_modules(self):
        return asyncio.run(super().active_modules())

    def difficulty(self):
        return asyncio.run(super().difficulty())

    def labels(self):
        return asyncio.run(super().labels())

    def seed(self):
        return asyncio.run(super().seed())

    # Request data from target
    def version(self, target):
        return asyncio.run(super().version(target))

    def module_info(self, target):
        return asyncio.run(super().module_info(target))

    def is_solved(self, target):
        return asyncio.run(super().is_solved(target))


class DebugBMP(SyncBMP):

    def _on_request(self, requester, msg_type):
        super()._on_request(requester, msg_type)
        print(f"{requester=} {msg_type=}")

    def _on_data(self, sender, msg_type, data):
        super()._on_data(sender, msg_type, data)
        print(f"{sender=} {msg_type=} {data=}")
