import gc
import random

try:
    from .helpers import title
except ImportError:
    from lib.helpers import title


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
""".replace("\n", "")
ROW_TEMPLATE = '<tr>{extra_td}<td class="simon-says-number">{strikes}</td>' \
    '<td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'
TABLE_TEMPLATE = """<table class="simon-says-table"><thead>
<tr>{extra_th}<th>#Strikes</th><th>Blue LED</th><th>Green LED</th><th>Red LED</th><th>Yellow LED</th><tr>
</thead><tbody>
{data_rows}
</tbody></table>""".replace("\n", "")

# Global cache of the current manual to avoid re-allocating large memory blocks
CURRENT_MANUAL: str = "\x00" * 6144

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

        random.seed()
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
        self.enabled = False
        self._generated_manual = False

    def log(self, msg: str):
        pass

    async def get_serial_no(self):
        raise NotImplementedError

    async def get_strikes(self):
        raise NotImplementedError

    async def strike(self):
        raise NotImplementedError

    async def next(self):
        raise NotImplementedError

    async def finish(self):
        raise NotImplementedError

    async def check_single_button(self, button: str, step = 0):
        if not self.enabled:
            return
        serial = any([True for c in await self.get_serial_no() if c.upper() in VOWELS])
        strikes = await self.get_strikes()
        current_mapping = self.mappings[serial][self.current_stage % len(self.mappings[serial])][strikes]
        if button != current_mapping[self.complete_output[step]]:
            self.log(f"Pre-check failed in stage {self.current_stage} with button {button} as step {step}.")
            if self._difficulty != "IMMORTAL":
                await self.strike()

    async def press_buttons(self, buttons: list):
        if not self.enabled:
            return
        serial = any([True for c in await self.get_serial_no() if c.upper() in VOWELS])
        strikes = await self.get_strikes()
        print(f"[DBG] {strikes=} {serial=} {self.current_stage=} {self.mappings=}")
        current_mapping = self.mappings[serial][self.current_stage % len(self.mappings[serial])][strikes]
        for i, button in enumerate(buttons):
            if button != current_mapping[self.complete_output[i]]:
                self.log(f"Check failed in step {i} with button {button}.")
                if self._difficulty != "IMMORTAL":
                    await self.strike()
                break
            self.log(f"Button {button} was correct.")
        else:
            self.current_stage += 1
            await self.next()
        if self.current_stage >= len(self.complete_output):
            await self.finish()

    def get_current_output(self) -> list:
        return self.complete_output[:self.current_stage + 1]

    def generate_manual(self) -> str:
        global CURRENT_MANUAL
        if self._generated_manual:
            return CURRENT_MANUAL

        def _make_table(vowel: bool, extra_th: str, extra_td: str) -> str:
            return TABLE_TEMPLATE.format(
                extra_th=extra_th,
                data_rows="\n".join([
                    "\n".join([
                        ROW_TEMPLATE.format(
                            title(mapping[strike]["BLUE"]),
                            title(mapping[strike]["GREEN"]),
                            title(mapping[strike]["RED"]),
                            title(mapping[strike]["YELLOW"]),
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

        del CURRENT_MANUAL
        gc.collect()
        CURRENT_MANUAL = MANUAL_TEMPLATE.format(
            num_buttons=len(self._colors),
            list_ext=list_ext,
            seq_len=self.difficulty[0],
            section_vowel=section_vowel,
            section_no_vowel=section_no_vowel
        )
        self._generated_manual = True
        return CURRENT_MANUAL
