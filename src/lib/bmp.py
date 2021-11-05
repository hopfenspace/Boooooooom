from micropython import const

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


def _parse_id(self, id_):
    id_ = bin(id_)[2:]
    return int(id_[0:4], 2), int(id_[4:8], 2), int(id_[8:16], 2), int(id_[16:17], 2)


class RequestableData:

    __slots__ = ("version", "module_info", "timer", "serial_number", "strikes", "max_strikes",
                 "modules", "active_modules", "difficulty", "labels", "is_solved")
    _slave2slave = ("version", "module_info", "is_solved")

    def __init__(self):
        for attr in self.__slots__:
            setattr(self, attr, None)
        for attr in self._slave2slave:
            data = {}
            for i in range(12):
                data[i] = None
            setattr(self, attr, data)


class BMP:

    def __init__(self, address):
        self.address = address

        self._callbacks = {}
        """functions taking the sender address, the data string and returning nothing"""
        self._callbacks[MSG_TIMER] = self._default_callback("timer")
        self._callbacks[MSG_SERIAL_NO] = self._default_callback("serial_number")
        self._callbacks[MSG_STRIKES] = self._default_callback("strikes")
        self._callbacks[MSG_MAX_STRIKES] = self._default_callback("max_strikes")
        self._callbacks[MSG_MODULE_COUNT] = self._default_callback("modules")
        self._callbacks[MSG_ACTIVE_MODULE_COUNT] = self._default_callback("active_modules")
        self._callbacks[MSG_DIFFICULTY] = self._default_callback("difficulty")
        self._callbacks[MSG_LABELS] = self._default_callback("labels")
        self._callbacks[MSG_VERSION] = self._default_callback("version")
        self._callbacks[MSG_MODULE_INFO] = self._default_callback("module_info")
        self._callbacks[MSG_IS_SOLVED] = self._default_callback("is_solved")

        self.request_handler = {}
        """function taking the sender address and returning nothing"""

        self._ongoing_data = {}
        """map from (sender, msg_type) to string"""

        self.data = RequestableData()
        """object the default callbacks store their data to"""

        can.on_receive(self._on_receive)

    def _on_receive(self, _):
        id_, ext, request, data_or_dlc = can.receive()
        sender, recipient, msg_type, eot = _parse_id(id_)
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
                if msg_type in self._callbacks:
                    self._callbacks[msg_type](sender, data)

    def _default_callback(self, attr):
        if attr not in RequestableData._slave2slave:
            def callback(_, data):
                setattr(self.data, attr, data)
        else:
            def callback(sender, data):
                getattr(self.data, attr)[sender] = data
        return callback

    def request(self, recipient, msg_type, callback=None):
        can.transmit(_format_id(recipient, msg_type), True, True, 0)
        if callback is not None:
            self._callbacks[msg_type] = callback

    def send(self, recipient, msg_type, data):
        packets = len(data) // 8
        if len(data) % 8 != 0:
            packets += 1
        for i in range(packets):
            eot = 1 if i == packets-1 else 0
            can.transmit(_format_id(recipient, msg_type, eot), True, False, data[i*8:])

    # Request action from master
    def register(self):
        self.request(MASTER, MSG_REGISTER)

    def strike(self):
        self.request(MASTER, MSG_STRIKE)

    def detonate(self):
        self.request(MASTER, MSG_DETONATE)

    def mark_solved(self):
        self.request(MASTER, MSG_MARK_SOLVED)

    def mark_reactivated(self):
        self.request(MASTER, MSG_MARK_REACTIVATED)

    def change_timer(self, timedelta):
        self.send(MASTER, MSG_CHANGE_TIMER, timedelta.to_bytes(4, "big", signed=True))
    
    def change_serial_no(self):
        self.request(MASTER, MSG_CHANGE_SERIAL_NO)

    # Request data from master
    def timer(self):
        self.request(MASTER, MSG_TIMER)

    def serial_no(self):
        self.request(MASTER, MSG_SERIAL_NO)

    def strikes(self):
        self.request(MASTER, MSG_STRIKES)

    def max_strikes(self):
        self.request(MASTER, MSG_MAX_STRIKES)

    def modules(self):
        self.request(MASTER, MSG_MODULE_COUNT)

    def active_modules(self):
        self.request(MASTER, MSG_ACTIVE_MODULE_COUNT)

    def difficulty(self):
        self.request(MASTER, MSG_DIFFICULTY)

    def labels(self):
        self.request(MASTER, MSG_LABELS)

    # Request data from target
    def version(self, target):
        self.request(target, MSG_VERSION)

    def module_info(self, target):
        self.request(target, MSG_MODULE_INFO)

    def is_solved(self, target):
        self.request(target, MSG_IS_SOLVED)
