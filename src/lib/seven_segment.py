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


class SevenSegment:

    __slots__ = ("shift_register", "most_significant_first")

    def __init__(self, shift_register):
        self.shift_register = shift_register
        self.most_significant_first = False  # if broken toggle this

    def write_digit(self, digit, dot=False):
        if dot:
            dot = 1
        else:
            dot = 0
        digit = str(digit).lower()
        self.shift_register.write_int(table[digit] << 1 + dot, most_significant_first=self.most_significant_first)

    def write_number(self, number, *, base=10):
        if base == 10:
            number = str(number)
        elif base == 2:
            number = bin(number)[2:]
        elif base == 8:
            number = oct(number)[2:]
        elif base == 16:
            number = hex(number)[2:]
        for digit in number:
            self.write_digit(digit)
