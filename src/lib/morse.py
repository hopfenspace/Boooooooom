import time
import uasyncio
from machine import Pin


international_morse_code = {
    "a": ".-", "b": "-...", "c": "-.-.", "d": "-..", "e": ".", "f": "..-.", "g": "--.", "h": "....", "i": "..",
    "j": ".---", "k": "-.-", "l": ".-..", "m": "--", "n": "-.", "o": "---", "p": ".--.", "q": "--.-", "r": ".-.",
    "s": "...", "t": "-", "u": "..-", "v": "...-", "w": ".--", "x": "-..-", "y": "-.--", "z": "--..", "1": ".----",
    "2": "..---", "3": "...--", "4": "....-", "5": ".....", "6": "-....", "7": "--...", "8": "---..", "9": "----.",
    "0": "-----", " ": "/"
}


class AsyncMorse:
    """Currently implemented are: a-z0-9 and ' '

    Value for unit_time is in ms.
    """
    def __init__(self, *, unit_time, pin):
        self.unit_time = unit_time
        self.morse_pin = Pin(pin, Pin.OUT, value=0)

    async def _dot(self):
        self.morse_pin.on()
        await uasyncio.sleep_ms(self.unit_time)
        self.morse_pin.off()

    async def _dash(self):
        self.morse_pin.on()
        await uasyncio.sleep_ms(self.unit_time * 3)
        self.morse_pin.off()

    async def _pause_word(self):
        await uasyncio.sleep_ms(self.unit_time * 7)

    async def _pause_intra_char(self):
        await uasyncio.sleep_ms(self.unit_time)

    async def _pause_inter_char(self):
        await uasyncio.sleep_ms(self.unit_time * 3)

    async def morse_once(self, sentence, *, end_with_word_pause=True):
        sentence = sentence.lower()
        morse_sentence = [international_morse_code[x] for x in sentence]
        for x in range(len(morse_sentence)):
            if "/" == morse_sentence[x]:
                await self._pause_word()
            for y in range(len(morse_sentence[x])):
                if "." == morse_sentence[x][y]:
                    await self._dot()
                elif "-" == morse_sentence[x][y]:
                    await self._dash()
                if y == len(morse_sentence[x]) - 1 and x != len(morse_sentence) - 1:
                    await self._pause_inter_char()
                else:
                    await self._pause_intra_char()
        if end_with_word_pause:
            await self._pause_word()

    async def morse_forever(self, sentence):
        while True:
            await self.morse_once(sentence, end_with_word_pause=True)


class Morse:
    """Currently implemented are: a-z0-9 and ' '

    Value for unit_time is in ms.
    """
    def __init__(self, *, unit_time):
        self.unit_time = unit_time
        self.morse_pin = None

    def _dot(self):
        self.morse_pin.on()
        time.sleep_ms(self.unit_time)
        self.morse_pin.off()

    def _dash(self):
        self.morse_pin.on()
        time.sleep_ms(self.unit_time * 3)
        self.morse_pin.off()

    def _pause_word(self):
        time.sleep_ms(self.unit_time * 7)

    def _pause_intra_char(self):
        time.sleep_ms(self.unit_time)

    def _pause_inter_char(self):
        time.sleep_ms(self.unit_time * 3)

    def write_morse(self, *, pin, sentence, end_with_word_pause=True):
        self.morse_pin = Pin(pin, Pin.OUT, value=0)

        sentence = sentence.lower()
        morse_sentence = [international_morse_code[x] for x in sentence]
        for x in range(len(morse_sentence)):
            if "/" == morse_sentence[x]:
                self._pause_word()
            for y in range(len(morse_sentence[x])):
                if "." == morse_sentence[x][y]:
                    self._dot()
                elif "-" == morse_sentence[x][y]:
                    self._dash()
                if y == len(morse_sentence[x]) - 1 and x != len(morse_sentence) - 1:
                    self._pause_inter_char()
                else:
                    self._pause_intra_char()
        if end_with_word_pause:
            self._pause_word()
