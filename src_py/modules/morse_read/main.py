import time
import random

from machine import Pin

from morse import Morse


class Difficulty:
    EASY = 320
    NORMAL = 160
    HARD = 80
    EXPERT = 40
    PREPARE_2_DIE = 20


class MorseReadGame:
    def __init__(self, *, difficulty, wordlist_count):
        self.difficulty = difficulty
        self.wordlist_count = wordlist_count

        wordlist = self._get_wordlist()
        frequency_list = set()
        while len(frequency_list) != len(wordlist):
            frequency_list.add(random.randint(1000, 2000))
        self.frequency_list = list(frequency_list)
        self.frequency_list.sort()
        self.wordlist_lookup = {}
        # Fill wordlist_lookup with kvp:    word: frequency
        [self.wordlist_lookup.__setitem__(wordlist[x], self.frequency_list[x]) for x in range(len(wordlist))]
        self.chosen_one = wordlist[random.randint(0, self.wordlist_count)]

        self.morse = Morse(unit_time=self.difficulty)

        self.pin_morse_led = 16
        self.led_strike = Pin(17, Pin.OUT)
        self.led_solved = Pin(5, Pin.OUT)

        self.button_left = Pin(4, Pin.IN)
        self.button_left.irq(handler=self.handle_left, trigger=Pin.IRQ_RISING)

        self.button_right = Pin(15, Pin.IN)
        self.button_right.irq(handler=self.handle_right, trigger=Pin.IRQ_RISING)

        self.button_submit = Pin(2, Pin.IN)
        self.button_submit.irq(handler=self.handle_submit, trigger=Pin.IRQ_RISING)

        self.current = self.wordlist_lookup[wordlist[random.randint(0, self.wordlist_count)]]
        self.solved = False

    def handle_left(self, *args, **kwargs):
        if not self.solved:
            current_index = self.frequency_list.index(self.current)
            if current_index != 0:
                self.current = self.wordlist_lookup[list(self.wordlist_lookup.keys())[current_index-1]]
                # TODO Set frequency to self.current

    def handle_right(self, *args, **kwargs):
        if not self.solved:
            current_index = self.frequency_list.index(self.current)
            if current_index != len(self.frequency_list)-1:
                self.current = self.wordlist_lookup[list(self.wordlist_lookup.keys())[current_index+1]]
                # TODO Set frequency to self.current

    def handle_submit(self, *args, **kwargs):
        if not self.solved:
            if self.wordlist_lookup[self.chosen_one] == self.current:
                # TODO Send solved
                self.led_solved.on()
                self.solved = True
            else:
                # TODO Send strike
                self.led_strike.on()
                time.sleep_ms(200)
                self.led_strike.off()

    def _get_wordlist(self):
        with open("wordlist.txt") as fh:
            words = [x.strip() for x in fh.readlines()]
            if self.difficulty >= 160:
                words = [x for x in words if len(x) == 5]
            start_index = random.randint(0, len(words)-self.wordlist_count)
            return words[start_index:start_index+self.wordlist_count]

    def start(self):
        # TODO Display current self.current frequency
        while not self.solved:
            self.morse.write_morse(
                pin=self.pin_morse_led,
                sentence=self.chosen_one,
                end_with_word_pause=True
            )


g = MorseReadGame(difficulty=Difficulty.NORMAL, wordlist_count=16)
g.start()
