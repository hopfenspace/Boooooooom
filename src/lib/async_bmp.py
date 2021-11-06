from micropython import const
import uasyncio

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


class BMP:

    def __init__(self, address):
        self.address = address

        self.request_handler = {}
        """function taking the sender address and returning nothing"""

        self._ongoing_data = {}
        """map from (sender, msg_type) to string"""

        self._requests = {}
        """Map from msg_type to ongoing request of that type"""
        self._lock = uasyncio.Lock()
        """Lock to sync write access to the _requests dict"""

        can.on_receive(self._on_receive)

    def _on_receive(self, _):
        id_, ext, request, data_or_dlc = can.receive()
        print(f"Parsed packet: id={id_}, ext={ext}, request={request}, data_or_dlc={data_or_dlc}")
        sender, recipient, msg_type, eot = _parse_id(id_)
        print(f"Parsed id: sender={sender}, recipient={recipient}, msg_type={msg_type}, eot={eot}")
        if recipient != self.address:
            return
        if request and msg_type in self.request_handler:
            self.request_handler[msg_type](sender)
        else:
            if (sender, msg_type) in self._ongoing_data:
                self._ongoing_data[(sender, msg_type)] += data_or_dlc
            else:
                self._ongoing_data[(sender, msg_type)] = data_or_dlc

            if eot:
                data = self._ongoing_data[(sender, msg_type)]
                del self._ongoing_data[(sender, msg_type)]

                if msg_type in self._requests:
                    request = self._requests[msg_type]
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
                request: _Request = requests[MSG_TIMER]
                # Check if the request has already finished
                new = request.event.is_set()
            except KeyError:
                # If there is no request yet, we have to create one
                new = True

            if new:
                # Create new request object
                request = _Request()
                requests[msg_type] = request

        if new:
            self.request(recipient, msg_type)

        await request.event.wait()
        return request.data

    async def send(self, recipient, msg_type, data):
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
