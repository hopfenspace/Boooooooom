#!/usr/bin/python3

import time
import random
import machine
import uasyncio
import micropython

micropython.alloc_emergency_exception_buf(128)

try:
    import bmp
    from simon_says import SimonSays
except ImportError:
    try:
        from lib import bmp
        from lib.simon_says import SimonSays
    except ImportError:
        from ...lib import bmp
        from ...lib.simon_says import SimonSays


class SimonSaysConsole(SimonSays):
    """
    Simon Says game usable in the interactive mode of Python for debugging
    """

    def __init__(self, difficulty: str, seed: int = None, max_strikes: int = 3):
        super().__init__(["BLUE", "GREEN", "RED", "YELLOW"], difficulty, seed or random.randint(0, 0xff), max_strikes)
        self.static_serial = "".join([random.choice("ABCDEFGHIJKLMNOPRSTUVWXYZ0123456789") for _ in range(8)])
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

    def play_interactively(self, manual_path: str):
        with open(manual_path, "w") as f:
            f.write(self.generate_manual())
        print(f"The manual is stored in {manual_path!r}")
        print(f"Strikes: {self.static_strikes}")
        print(f"Serial no: {self.static_serial}")
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

    def __init__(self, bmp_: bmp.AsyncBMP, difficulty: str, button_setup: dict, seed: int, max_strikes: int = 3):
        super().__init__(list(button_setup.keys()), difficulty, seed, max_strikes)
        self._bmp = bmp_
        self.buttons = button_setup
        self.current_task = None

        def handle_b(_): self.handle("BLUE")
        def handle_g(_): self.handle("GREEN")
        def handle_r(_): self.handle("RED")
        def handle_y(_): self.handle("YELLOW")

        self.buttons["BLUE"]["in"].irq(handler=handle_b, trigger=machine.Pin.IRQ_RISING)
        self.buttons["GREEN"]["in"].irq(handler=handle_g, trigger=machine.Pin.IRQ_RISING)
        self.buttons["RED"]["in"].irq(handler=handle_r, trigger=machine.Pin.IRQ_RISING)
        self.buttons["YELLOW"]["in"].irq(handler=handle_y, trigger=machine.Pin.IRQ_RISING)

    # This coroutine should be run as a task which could be cancelled on user input
    async def blink(self, wait_before_restart: bool = False):
        if not self.enabled:
            return
        if wait_before_restart:
            await uasyncio.sleep_ms(self.LED_RESTART_TIME_MS)
        for c in self.get_current_output():
            self.buttons[c]["out"].value(1)
            await uasyncio.sleep_ms(self.LED_FLASH_TIME_MS)
            self.buttons[c]["out"].value(0)
            await uasyncio.sleep_ms(self.LED_BETWEEN_TIME_MS)
        await uasyncio.sleep_ms(self.LED_REPEAT_TIME_MS)
        self.current_task = uasyncio.get_event_loop().create_task(self.blink())

    def start(self):
        if self.current_task:
            self.current_task.cancel()
        self.enabled = True
        self.current_task = uasyncio.get_event_loop().create_task(self.blink())

    def stop(self):
        self.enabled = False
        self.current_task.cancel()
        for c in self.buttons:
            self.buttons[c]["out"].value(0)

    def handle(self, color: str):
        if not self.enabled:
            return
        button = self.buttons[color]
        if button["in"].value():
            button["out"].on()
            if button["state"] == 0:
                self.current_task.cancel()
                for c in self.buttons:
                    if c != color:
                        self.buttons[c]["out"].value(0)
                uasyncio.get_event_loop().create_task(self.press_button(button["color"]))
                self.current_task = uasyncio.get_event_loop().create_task(self.blink(True))
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
        print("Now press all the buttons! Starting an active loop for 30s...")
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
    def create_buttons_from_pin_setup(
            cls,
            blue: (machine.Pin, machine.Pin),
            green: (machine.Pin, machine.Pin),
            red: (machine.Pin, machine.Pin),
            yellow: (machine.Pin, machine.Pin)
    ) -> dict:
        return {
            "BLUE": {"in": blue[0], "out": blue[1], "color": "BLUE", "state": 0},
            "GREEN": {"in": green[0], "out": green[1], "color": "GREEN", "state": 0},
            "RED": {"in": red[0], "out": red[1], "color": "RED", "state": 0},
            "YELLOW": {"in": yellow[0], "out": yellow[1], "color": "YELLOW", "state": 0}
        }


# Adapt this function according to the used hardware & wire setup
def get_buttons_by_setup() -> dict:
    return SimonSaysGame.create_buttons_from_pin_setup(
        (machine.Pin(blue_button_pin, machine.Pin.IN), machine.Pin(blue_led_pin, machine.Pin.OUT)),
        (machine.Pin(green_button_pin, machine.Pin.IN), machine.Pin(green_led_pin, machine.Pin.OUT)),
        (machine.Pin(red_button_pin, machine.Pin.IN), machine.Pin(red_led_pin, machine.Pin.OUT)),
        (machine.Pin(yellow_button_pin, machine.Pin.IN), machine.Pin(yellow_led_pin, machine.Pin.OUT)),
    )


class SimonSaysGameWrapper:
    """
    Wrapper around the SimonSaysGame class to enable proper startup & shutdown

    This class should be considered a singleton.
    """

    def __init__(self):
        self.address: int = 12  # TODO: this must be read via/from hardware
        self.game = None
        self.bmp = bmp.AsyncBMP(self.address)

        self.bmp.request_handler[bmp.MSG_INIT] = self.handle_init
        self.bmp.request_handler[bmp.MSG_RESET] = self.handle_init
        self.bmp.request_handler[bmp.MSG_START] = self.handle_start
        self.bmp.request_handler[bmp.MSG_RTFM] = self.handle_rtfm
        self.bmp.request_handler[bmp.MSG_DEFUSED] = self.handle_defused
        self.bmp.request_handler[bmp.MSG_EXPLODED] = self.handle_exploded
        self.bmp.request_handler[bmp.MSG_VERSION] = self.handle_version
        self.bmp.request_handler[bmp.MSG_MODULE_INFO] = self.handle_module_info
        self.bmp.request_handler[bmp.MSG_BLACKOUT] = self.handle_blackout
        self.bmp.request_handler[bmp.MSG_IS_SOLVED] = self.handle_is_solved

    def handle_init(self, _):
        if self.game is not None:
            self.game.stop()
        uasyncio.get_event_loop().create_task(self.init())

    def handle_start(self, _):
        if not self.game:
            uasyncio.run(self.init())
        self.game.start()

    def handle_rtfm(self, _):
        uasyncio.get_event_loop().create_task(self.bmp.send(bmp.MASTER, bmp.MSG_RTFM, self.game.generate_manual()))

    def handle_defused(self, _):
        print("Not implemented: handle_defused")

    def handle_exploded(self, _):
        print("Not implemented: handle_exploded")

    def handle_version(self, _):
        print("Not implemented: handle_version")

    def handle_module_info(self, _):
        print("Not implemented: handle_module_info")

    def handle_blackout(self, _):
        print("Not implemented: handle_blackout")

    def handle_is_solved(self, _):
        print("Not implemented: handle_is_solved")

    async def init(self):
        if self.game is not None:
            self.game.stop()
        self.game = None
        seed = await self.bmp.seed()
        difficulty = await self.bmp.difficulty()
        max_strikes = await self.bmp.max_strikes()
        self.game = SimonSaysGame(self.bmp, difficulty, get_buttons_by_setup(), seed, max_strikes)

    async def main(self):
        self.bmp.register()
        while True:
            uasyncio.sleep(60)
