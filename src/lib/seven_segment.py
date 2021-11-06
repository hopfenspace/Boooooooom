from shift_register import ShiftRegister7648


table = {
    " ": 0x00,
    "0": 0x7E,
    "1": 0x30,
    "2": 0x6D,
    "3": 0x79,
    "4": 0x33,
    "5": 0x5B,
    "6": 0x5F,
    "7": 0x70,
    "8": 0x7F,
    "9": 0x7B,  # The actual characters are:
    "a": 0x77,  # A
    "b": 0x1F,  # b
    "c": 0x4E,  # C
    "d": 0x3D,  # d
    "e": 0x4F,  # E
    "f": 0x47,  # F
}


class SevenSegment(ShiftRegister7648):

    def set(self, digit, dot=False):
        if dot:
            dot = 1
        else:
            dot = 0
        digit = str(digit.lower())
        self.write_int(table[digit] << 1 + dot)
        # starting from left the binary digits represent:
        # a, b, c, d, e, f, g, dot
