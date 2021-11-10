#!/usr/bin/python3

import time
import random
import machine
import uasyncio
import micropython

micropython.alloc_emergency_exception_buf(128)

NL = "\n"
VOWELS = "AEIOU"
ALPHABET = "ABCDEFGHIJKLMNOPRSTUVWXYZ0123456789"


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
        super().__init__(["BLUE", "GREEN", "RED", "YELLOW"], difficulty)
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


class SimonSaysGame(SimonSays):
    """
    Simon Says game using hardware pins to configure interrupt handlers
    """

    LED_FLASH_TIME_MS = 400  # duration the LED is on
    LED_BETWEEN_TIME_MS = 400  # duration between two LED flashes
    LED_REPEAT_TIME_MS = 2000  # duration before repeating the LED flashing
    LED_RESTART_TIME_MS = 3000  # duration before restarting the LED flashing after user input

    def __init__(self, difficulty: str, button_setup: dict):
        super().__init__(list(button_setup.keys()), difficulty)
        self.buttons = button_setup

        def handle_b(_): self.handle("BLUE")
        def handle_g(_): self.handle("GREEN")
        def handle_r(_): self.handle("RED")
        def handle_y(_): self.handle("YELLOW")

        self.buttons["BLUE"]["in"].irq(handler=handle_b, trigger=machine.Pin.IRQ_RISING)
        self.buttons["GREEN"]["in"].irq(handler=handle_g, trigger=machine.Pin.IRQ_RISING)
        self.buttons["RED"]["in"].irq(handler=handle_r, trigger=machine.Pin.IRQ_RISING)
        self.buttons["YELLOW"]["in"].irq(handler=handle_y, trigger=machine.Pin.IRQ_RISING)

        self.current_task = uasyncio.get_event_loop().create_task(self.blink())

    # This coroutine should be run as a task which could be cancelled on user input
    async def blink(self):
        for c in self.get_current_output():
            self.buttons[c]["out"].value(1)
            await uasyncio.sleep_ms(self.LED_FLASH_TIME_MS)
            self.buttons[c]["out"].value(0)
            await uasyncio.sleep_ms(self.LED_BETWEEN_TIME_MS)
        await uasyncio.sleep_ms(self.LED_REPEAT_TIME_MS)
        self.current_task = uasyncio.get_event_loop().create_task(self.blink())

    # This coroutine should be run as a task which could be cancelled on user input
    async def restart_blinking(self):
        await uasyncio.sleep_ms(self.LED_RESTART_TIME_MS)
        self.current_task = uasyncio.get_event_loop().create_task(self.blink())

    def handle(self, color: str):
        button = self.buttons[color]
        if button["in"].value():
            button["out"].on()
            if button["state"] == 0:
                self.current_task.cancel()
                for c in self.buttons:
                    if c != color:
                        self.buttons[c]["out"].value(0)
                uasyncio.get_event_loop().create_task(self.press_button(button["color"]))
                self.current_task = uasyncio.get_event_loop().create_task(self.restart_blinking())
            button["state"] = 1
        else:
            button["out"].off()
            button["state"] = 0

    def test_hardware(self):
        print("Checking the LED outputs...")
        for color in self.buttons:
            print(f"You should see the {color} LED.")
            led = self.buttons[color]["out"]
            led.on()
            time.sleep(2)
            led.off()
            time.sleep(1)
        print("Now press all the buttons! Starting an active for 30s loop...")
        start_time = time.ticks_ms()
        while True:
            for color in self.buttons:
                self.buttons[color]["out"].value(self.buttons[color]["in"].value())
                if self.buttons[color]["in"].value():
                    print(f"Button {color} is pressed.")
            if time.ticks_diff(time.ticks_ms(), start_time) > 30 * 10**3:
                break
        print("Done.")

    @classmethod
    def create_from_pin_setup(
            cls,
            difficulty: str,
            blue: (machine.Pin, machine.Pin),
            green: (machine.Pin, machine.Pin),
            red: (machine.Pin, machine.Pin),
            yellow: (machine.Pin, machine.Pin)
    ):
        buttons = {
            "BLUE": {
                "in": blue[0],
                "out": blue[1],
                "color": "BLUE",
                "state": 0
            },
            "GREEN": {
                "in": green[0],
                "out": green[1],
                "color": "GREEN",
                "state": 0
            },
            "RED": {
                "in": red[0],
                "out": red[1],
                "color": "RED",
                "state": 0
            },
            "YELLOW": {
                "in": yellow[0],
                "out": yellow[1],
                "color": "YELLOW",
                "state": 0
            }
        }
        return SimonSaysGame(difficulty, buttons)

    @classmethod
    def create_from_pin_ids(
            cls,
            difficulty: str,
            blue_button_pin: int,
            blue_led_pin: int,
            green_button_pin: int,
            green_led_pin: int,
            red_button_pin: int,
            red_led_pin: int,
            yellow_button_pin: int,
            yellow_led_pin: int
    ):
        blue = (machine.Pin(blue_button_pin, machine.Pin.IN), machine.Pin(blue_led_pin, machine.Pin.OUT))
        green = (machine.Pin(green_button_pin, machine.Pin.IN), machine.Pin(green_led_pin, machine.Pin.OUT))
        red = (machine.Pin(red_button_pin, machine.Pin.IN), machine.Pin(red_led_pin, machine.Pin.OUT))
        yellow = (machine.Pin(yellow_button_pin, machine.Pin.IN), machine.Pin(yellow_led_pin, machine.Pin.OUT))
        return SimonSaysGame.create_from_pin_setup(difficulty, blue, green, red, yellow)
