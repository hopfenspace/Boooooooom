try:
    import uasyncio as asyncio
except ImportError:
    import asyncio
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
        await asyncio.sleep_ms(self.unit_time)
        self.morse_pin.off()

    async def _dash(self):
        self.morse_pin.on()
        await asyncio.sleep_ms(self.unit_time * 3)
        self.morse_pin.off()

    async def _pause_word(self):
        await asyncio.sleep_ms(self.unit_time * 7)

    async def _pause_intra_char(self):
        await asyncio.sleep_ms(self.unit_time)

    async def _pause_inter_char(self):
        await asyncio.sleep_ms(self.unit_time * 3)

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


class Morse(AsyncMorse):

    def morse(self, sentence, *, end_with_word_pause=True):
        asyncio.run(super().morse_once(sentence, end_with_word_pause=end_with_word_pause))
