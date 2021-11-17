#!/usr/bin/python3

import can
import time
import random
import machine
import uasyncio
import micropython

micropython.alloc_emergency_exception_buf(128)

try:
    import bmp
    import module
    from simon_says import SimonSays
except ImportError:
    try:
        from lib import bmp
        from lib import module
        from lib.simon_says import SimonSays
    except ImportError:
        from ...lib import bmp
        from ...lib import module
        from ...lib.simon_says import SimonSays


class SimonSaysConsole(SimonSays):
    """
    Simon Says game usable in the interactive mode of Python for debugging
    """

    def __init__(self, difficulty: str, seed: int = None, max_strikes: int = 3):
        super().__init__(["BLUE", "GREEN", "RED", "YELLOW"], difficulty, seed or random.randint(0, 0xff), max_strikes)
        self.static_serial = "".join([random.choice("ABCDEFGHIJKLMNOPRSTUVWXYZ0123456789") for _ in range(8)])
        self.static_strikes = random.randint(0, 2)
        self.finished = False

    async def get_serial_no(self):
        return self.static_serial

    async def get_strikes(self):
        return self.static_strikes

    async def strike(self):
        print("STRIKE!")

    async def next(self):
        print("NEXT!")

    async def finish(self):
        print("FINISH!")
        self.finished = True

    def play_interactively(self, manual_path: str):
        with open(manual_path, "w") as f:
            f.write(self.generate_manual())
        print(f"The manual is stored in: {manual_path}")
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

    def log(self, msg: str):
        print(f"SimonSays({self._bmp.address}) [{time.ticks_ms()/1000:.3f}]: {msg}")

    async def get_serial_no(self):
        return await self._bmp.serial_no()

    async def get_strikes(self):
        return await self._bmp.strikes()

    async def strike(self):
        self.log("Strike!")
        self._bmp.strike()
        if self.current_task:
            self.current_task.cancel()
        self.current_task = uasyncio.get_event_loop().create_task(self.blink(True))

    async def next(self):
        self.log(f"Solved stage {self.current_stage - 1}!")
        if self.current_task:
            self.current_task.cancel()
        self.current_task = uasyncio.get_event_loop().create_task(self.blink(True))

    async def finish(self):
        self.log("Module has been finished!")
        self.stop()
        self._bmp.mark_solved()

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
        self.log("Starting module...")
        if self.current_task:
            self.current_task.cancel()
        self.enabled = True
        self.current_task = uasyncio.get_event_loop().create_task(self.blink())

    def stop(self):
        self.log("Stopping module...")
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
                self.log(f"Pressing button '{color}'!")
                uasyncio.get_event_loop().create_task(self.press_button(button["color"]))
                self.current_task = uasyncio.get_event_loop().create_task(self.blink(True))
            button["state"] = 1
        else:
            button["out"].off()
            button["state"] = 0

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


# Use this function to ensure the setup generated by get_buttons_by_setup works correctly
def test_hardware_setup(buttons: dict):
    print("Checking the LED outputs...")
    for color in buttons:
        print(f"You should see the {color} LED.")
        led = buttons[color]["out"]
        led.on()
        time.sleep(2)
        led.off()
        time.sleep(1)
    print("Now press all the buttons! Starting an active loop for 30s...")
    start_time = time.ticks_ms()
    while time.ticks_diff(time.ticks_ms(), start_time) < 30 * 10**3:
        for color in buttons:
            value = buttons[color]["in"].value()
            buttons[color]["out"].value(value)
            if value:
                if buttons[color]["state"] == 0:
                    print(f"Detected {color} button press.")
                buttons[color]["state"] = 1
            else:
                if buttons[color]["state"] == 1:
                    print(f"Detected {color} button release.")
                buttons[color]["state"] = 0
    for color in buttons:
        buttons[color]["out"].value(0)
        buttons[color]["state"] = 0
    print("Done.")


class SimonSaysGameWrapper(module.DebugModule):
    """
    Wrapper around the SimonSaysGame class to enable proper startup & shutdown

    This class should be considered a singleton.
    """

    def __init__(self, address: int):
        super().__init__(address)
        self.address = address
        self.game = None

    async def on_init(self, _):
        if self.game is not None:
            self.game.stop()
        await super().on_init(_)
        self.bmp.register()
        self.game = None
        # seed = await self.bmp.seed()
        seed = 0x1337  # TODO: await the implementation of MSG_SEED
        difficulty = bmp.DIFFICULTY_NAMES[await self.bmp.difficulty()]
        max_strikes = await self.bmp.max_strikes()
        print(f"Using seed={seed}, difficulty={difficulty}, max_strikes={max_strikes}!")
        self.game = SimonSaysGame(self.bmp, difficulty, get_buttons_by_setup(), seed, max_strikes)

    async def on_start(self, _):
        await super().on_start(_)
        self.game.start()

    async def on_rtfm(self, _):
        await super().on_rtfm(_)
        uasyncio.get_event_loop().create_task(self.bmp.send(bmp.MASTER, bmp.MSG_RTFM, self.game.generate_manual()))


# Main function to be executed to start the program
def main():
    print("Starting main program ...")
    try:
        can.stop()
    except RuntimeError:
        pass
    can.start(1000)
    module_address = 12  # TODO: this must be read via/from hardware
    # uasyncio.get_event_loop().set_exception_handler(handle_exc)
    wrapper = SimonSaysGameWrapper(module_address)
    print("Running main task ...")
    uasyncio.run(wrapper.run())


# main()
