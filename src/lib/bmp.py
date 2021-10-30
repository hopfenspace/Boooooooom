from micropython import const

import can


_reserved = 0

MASTER = const(0x00)

MSG_RESET = const(0x00)
MSG_INIT = const(0x01)
MSG_START = const(0x02)
MSG_DEFUSED = const(0x03)
MSG_EXPLODED = const(0x04)
MSG_RTFM = const(0x05)
MSG_VERSION = const(0x06)
MSG_MODULE_INFO = const(0x07)
MSG_REGISTER = const(0x08)
MSG_STRIKE = const(0x09)
MSG_DETONATE = const(0x0a)
MSG_MARK_SOLVED = const(0x0b)
MSG_MARK_REACTIVATED = const(0x0c)
MSG_CHANGE_TIMER = const(0x0d)
MSG_CHANGE_SERIAL_NO = const(0x0e)


class BMP:

    def __init__(self, address):
        self.address = address
        self.callbacks = {}
        """functions taking the sender address, the data string and returning nothing"""
        self.request_handler = {}
        """function taking the sender address and returning nothing"""
        self.ongoing_data = {}
        can.on_receive(self._on_receive)

    def _format_id(self, recipient, msg_type, eot=1):
        return ((((((self.address << 4) + recipient) << 8) + msg_type) << 1) + eot) << 12

    def _parse_id(self, id_):
        id_ = bin(id_)[2:]
        sender = int(id_[0:4], 2)
        recipient = int(id_[4:8], 2)
        msg_type = int(id_[8:16], 2)
        eot = int(id_[16:17], 2)
        return sender, recipient, msg_type, eot

    def _on_receive(self, _):
        id_, ext, request, data_or_dlc = can.receive()
        sender, recipient, msg_type, eot = self._parse_id(id_)
        if recipient != self.address:
            return
        if request and msg_type in self.request_handler:
            self.request_handler[msg_type](sender)
        else:
            if (sender, msg_type) in self.ongoing_data:
                self.ongoing_data[(sender, msg_type)] += data_or_dlc
            else:
                self.ongoing_data[(sender, msg_type)] = data_or_dlc

            if eot:
                data = self.ongoing_data[(sender, msg_type)]
                del self.ongoing_data[(sender, msg_type)]
                if msg_type in self.callbacks:
                    self.callbacks[msg_type](sender, data)

    def request(self, recipient, msg_type, callback=None):
        can.transmit(self._format_id(recipient, msg_type), True, True, 0)
        if callback is not None:
            self.callbacks[msg_type] = callback

    def send(self, recipient, msg_type, data):
        packets = len(data) // 8
        if len(data) % 8 != 0:
            packets += 1
        for i in range(packets):
            eot = 1 if i == packets-1 else 0
            can.transmit(self._format_id(recipient, msg_type, eot), True, False, data[i*8:])

    # BMP methods
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
        if timedelta < 0:
            timedelta = (2**32) - timedelta
        data = ["\0", "\0", "\0", "\0"]
        for i in range(4):
            data[3-i] = chr((timedelta & (0xFF << (i*8))) >> (i*8))
        self.send(MASTER, MSG_CHANGE_TIMER, "".join(data))
    
    def change_serial_no(self):
        self.request(MASTER, MSG_CHANGE_SERIAL_NO)
    