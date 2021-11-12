import random


VOWELS = "AEIOU"

MANUAL_TEMPLATE = """<div class="simon-says"><h2>Simon Says</h2>
<!-- even though it's crappy design, it's the easiest way to style our tables properly -->
<style>
.simon-says table, .simon-says th, .simon-says td {{ border: 1px solid black; border-collapse: collapse; }}
.simon-says th {{ padding: 4px 16px; }}
.simon-says td {{ padding: 1px 4px; }}
.simon-says td.simon-says-number {{ text-align: center; }}
</style>
<ol>
<li>One of the {num_buttons} colored buttons will flash.</li>
<li>Using the correct table below, press the button with the corresponding color.</li>
<li>The original button will flash, followed by another. Repeat this sequence in order using the color mapping.</li>
<li>The sequence will lengthen by one each time you correctly enter a sequence until the module is disarmed.</li>
{list_ext}
<li>The whole sequence contains {seq_len} stages in total.</li>
</ol>
<h3>The serial number currently <u>does</u> contain a vowel</h3>
{section_vowel}
<h3>The serial number currently <u>does not</u> contain a vowel</h3>
{section_no_vowel}</div>
"""
ROW_TEMPLATE = '<tr>{extra_td}<td class="simon-says-number">{strikes}</td>' \
    '<td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'
TABLE_TEMPLATE = """<table class="simon-says-table"><thead>
<tr>{extra_th}<th>#Strikes</th><th>Blue LED</th><th>Green LED</th><th>Red LED</th><th>Yellow LED</th><tr>
</thead><tbody>
{data_rows}
</tbody></table>"""


class SimonSays:
    """
    Simon Says core game without implemented interaction methods
    """

    # Mapping from difficulty to number of colors and number of different color mappings
    DIFFICULTIES = {
        "IMMORTAL": (4, 1),
        "TRAINING": (2, 1),
        "EASY": (3, 1),
        "NORMAL": (4, 1),
        "HARD": (4, 2),
        "EXPERT": (6, 2),
        "PREPARE_2_DIE": (7, 6)
    }

    def __init__(self, colors: list, difficulty: str, seed: int, max_strikes: int):
        self._colors = colors
        self._difficulty = difficulty
        self._seed = seed
        self._max_strikes = max_strikes
        self.difficulty = self.DIFFICULTIES[difficulty]
        self.complete_output = [random.choice(self._colors) for _ in range(self.difficulty[0])]

        random.seed(self._seed)

        def _shuffle(lst):
            for i in reversed(range(1, len(lst))):
                j = int(random.random() * (i + 1))
                lst[i], lst[j] = lst[j], lst[i]
            return lst

        self.mappings = {
            k: [
                {
                    s: dict(zip(list(self._colors), _shuffle(self._colors)))
                    for s in range(self._max_strikes)
                }
                for _ in range(self.difficulty[1])  # Number of difficulties
            ]
            for k in (0, 1)  # Vowel in serial no.?
        }

        self.current_stage = 0
        self.current_step = 0
        self.finished = False
        self.enabled = False

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
        if not self.enabled:
            return
        serial = any([True for c in await self.get_serial_no() if c.upper() in VOWELS])
        strikes = await self.get_strikes()
        current_mapping = self.mappings[serial][self.current_step % len(self.mappings[serial])][strikes]
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
        def _make_table(vowel: bool, extra_th: str, extra_td: str) -> str:
            return TABLE_TEMPLATE.format(
                extra_th=extra_th,
                data_rows="\n".join([
                    "\n".join([
                        ROW_TEMPLATE.format(
                            mapping[strike]["BLUE"].title(),
                            mapping[strike]["GREEN"].title(),
                            mapping[strike]["RED"].title(),
                            mapping[strike]["YELLOW"].title(),
                            extra_td=extra_td.format(i+1),
                            strikes=strike
                        )
                        for strike in mapping
                    ])
                    for i, mapping in enumerate(self.mappings[vowel])
                ])
            )

        if self.difficulty[1] > 1:
            list_ext = "<li>There are multiple color mappings below, which must be iterated in every stage.</li>\n"
            list_ext += "<li>This iteration will start over again at the beginning of the sequence.</li>"
            section_no_vowel = _make_table(False, "<th>#Step</th>", '<td class="simon-says-number">{}</td>')
            section_vowel = _make_table(True, "<th>#Step</th>", '<td class="simon-says-number">{}</td>')

        else:
            list_ext = ""
            section_no_vowel = _make_table(False, "", "")
            section_vowel = _make_table(True, "", "")

        return MANUAL_TEMPLATE.format(
            num_buttons=len(self._colors),
            list_ext=list_ext,
            seq_len=self.difficulty[0],
            section_vowel=section_vowel,
            section_no_vowel=section_no_vowel
        )
