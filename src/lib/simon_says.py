import random


VOWELS = "AEIOU"


class SimonSays:
    """
    Simon Says core game without implemented interaction methods
    """

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

    def __init__(self, colors: list, difficulty: str):
        self._colors = colors
        self._difficulty = difficulty
        self.difficulty = self.DIFFICULTIES[difficulty]
        self.complete_output = [random.choice(self._colors) for _ in range(self.difficulty[0])]

        def _shuffle(lst):
            for i in reversed(range(1, len(lst))):
                j = int(random.random() * (i + 1))
                lst[i], lst[j] = lst[j], lst[i]
            return lst

        self.mappings = [
            {
                k: dict(zip(list(self._colors), _shuffle(self._colors)))
                for k in [(0, True), (1, True), (2, True), (0, False), (1, False), (2, False)]
            }
            for _ in range(self.difficulty[1])
        ]

        self.current_stage = 0
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
            if self.current_step >= self.current_stage + 1:
                self.current_stage += 1
                self.current_step = 0
                await self.next()
            if self.current_stage >= len(self.complete_output):
                self.finished = True
                await self.finish()

    def get_current_output(self) -> list:
        return self.complete_output[:self.current_step + 1]

    def generate_manual(self) -> str:
        pass  # TODO
