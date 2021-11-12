from micropython import const
import uasyncio
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


class _Request:
    __slots__ = ("event", "data")

    def __init__(self):
        self.event = uasyncio.Event()
        self.data = None


class AsyncBMP:

    def __init__(self, address):
        self.address = address

        self.request_handler = {}
        """function taking the sender address and returning nothing"""

        self._ongoing_data = {}
        """map from (sender, msg_type) to string"""

        self._requests = {}
        """Map from (msg_type, target) to ongoing request to that target of that type"""
        self._lock = uasyncio.Lock()
        """Lock to sync write access to the _requests dict"""

        can.on_receive(self._on_receive)

    def _on_receive(self, _):
        id_, ext, request, data_or_dlc = can.receive()
        sender, recipient, msg_type, eot = _parse_id(id_)
        # print(f"Parsed packet: {sender=}, {recipient=}, {msg_type=}, {eot=}, {ext=}, {request=}, {repr(data_or_dlc)=}")
        if recipient != self.address:
            return
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
            uasyncio.create_task(self.request_handler[msg_type](requester))

    def _on_data(self, sender, msg_type, data):
        # TODO handle request to multiple devices!!!
        if (msg_type, sender) in self._requests:
            request = self._requests[(msg_type, sender)]
            if not request.event.is_set():
                request.data = data

                async def set_event():
                    request.event.set()

                uasyncio.run(set_event())

    def request(self, recipient, msg_type):
        # Just send the request over can
        can.transmit(_format_id(self.address, recipient, msg_type), True, True, 0)

    async def request_data(self, recipient, msg_type):
        requests: dict = self._requests  # Reduce lookups while holding the lock

        async with self._lock:
            try:
                # Get the current request
                request: _Request = requests[(msg_type, recipient)]
                # Check if the request has already finished
                new = request.event.is_set()
            except KeyError:
                # If there is no request yet, we have to create one
                new = True

            if new:
                # Create new request object
                request = _Request()
                requests[(msg_type, recipient)] = request

        if new:
            self.request(recipient, msg_type)

        await request.event.wait()
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
        self.send(MASTER, MSG_CHANGE_TIMER, timedelta.to_bytes(4, "big"))

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
        return uasyncio.run(super().timer())

    def serial_no(self):
        return uasyncio.run(super().serial_no())

    def strikes(self):
        return uasyncio.run(super().strikes())

    def max_strikes(self):
        return uasyncio.run(super().max_strikes())

    def modules(self):
        return uasyncio.run(super().modules())

    def active_modules(self):
        return uasyncio.run(super().active_modules())

    def difficulty(self):
        return uasyncio.run(super().difficulty())

    def labels(self):
        return uasyncio.run(super().labels())

    # Request data from target
    def version(self, target):
        return uasyncio.run(super().version(target))

    def module_info(self, target):
        return uasyncio.run(super().module_info(target))

    def is_solved(self, target):
        return uasyncio.run(super().is_solved(target))

