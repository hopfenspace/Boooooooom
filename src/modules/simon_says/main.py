#!/usr/bin/python3

import random
import machine
import uasyncio


NL = "\n"
VOWELS = "AEIOU"
ALPHABET = "ABCDEFGHIJKLMNOPRSTUVWXYZ0123456789"


class SimonSays:
    """
    Simon Says core game without implemented interaction methods
    """

    # Mapping to define the different color names
    COLORS = {
        "BLUE": 1,
        "GREEN": 2,
        "RED": 3,
        "YELLOW": 4
    }

    # Mapping from difficulty to number of colors and number of different color mappings
    DIFFICULTIES = {
        "IMMORTAL": (1, 1),
        "TRAINING": (2, 1),
        "EASY": (3, 1),
        "NORMAL": (4, 1),
        "HARD": (4, 2),
        "EXPERT": (6, 2),
        "PREPARE_2_DIE": (6, 6)
    }

    def __init__(self, difficulty: str):
        self._difficulty = difficulty
        self.difficulty = self.DIFFICULTIES[difficulty]
        self.complete_output = [random.choice(list(self.COLORS)) for _ in range(self.difficulty[0])]

        def _shuffle(lst):
            for i in reversed(range(1, len(lst))):
                j = int(random.random() * (i + 1))
                lst[i], lst[j] = lst[j], lst[i]
            return lst

        self.mappings = [
            {
                k: dict(zip(list(self.COLORS.keys()), _shuffle(list(self.COLORS.keys()))))
                for k in [(0, True), (1, True), (2, True), (0, False), (1, False), (2, False)]
            }
            for _ in range(self.difficulty[1])
        ]

        self.current_step = 0
        self.finished = False

    async def get_serial_no(self):
        raise NotImplementedError

    async def get_strikes(self):
        raise NotImplementedError

    async def strike(self):
        raise NotImplementedError

    async def reset(self):
        raise NotImplementedError

    async def next(self):
        raise NotImplementedError

    async def finish(self):
        raise NotImplementedError

    async def press_button(self, button: str):
        serial = any([True for c in await self.get_serial_no() if c.upper() in VOWELS])
        strikes = await self.get_strikes()
        current_mapping = self.mappings[self.current_step % len(self.mappings)][(strikes, serial)]
        if button != current_mapping[self.complete_output[self.current_step]]:
            self.current_step = 0
            if self._difficulty != "IMMORTAL":
                await self.strike()
            await self.reset()
        else:
            self.current_step += 1
            if self.current_step >= len(self.complete_output):
                self.finished = True
                await self.finish()
            else:
                await self.next()

    def get_current_output(self) -> list:
        return self.complete_output[:self.current_step + 1]

    def generate_manual(self) -> str:
        pass  # TODO


class SimonSaysConsole(SimonSays):
    """
    Simon Says game usable in the interactive mode of Python for debugging
    """

    def __init__(self, difficulty: str):
        super().__init__(difficulty)
        self.static_serial = "".join([random.choice(ALPHABET) for _ in range(8)])
        self.static_strikes = random.randint(0, 2)

    async def get_serial_no(self):
        return self.static_serial

    async def get_strikes(self):
        return self.static_strikes

    async def strike(self):
        print("STRIKE!")

    async def reset(self):
        pass

    async def next(self):
        print("NEXT!")

    async def finish(self):
        print("FINISH!")

    def play_interactively(self):
        print(f"Strikes: {self.static_strikes}")
        print(f"Serial no: {self.static_serial}")
        print(f"Mappings:\n{NL.join(str(mapping) for mapping in self.mappings)}")
        while not self.finished:
            print(" - ".join(self.get_current_output()))
            color = input("> ").upper()
            uasyncio.run(self.press_button(color))
