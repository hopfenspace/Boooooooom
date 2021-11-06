# Can Module

## Basic Example
```python
>>> import can
>>> can.start(1000)
>>> can.transmit(1337, True, False, "Hello!")
>>> can.transmit(1338, True, True, 8)
>>> can.receive()
(1338, True, False, "Wololo<3")
>>> can.stop()
```

## Methods

### `set_pins(tx, rx)`
Specify the pins to use.
Defaults to 5 and 4.
This must be called before `start` to take effect.

### `start(baudrate: int)`
Start the can module. The baudrate specifies kbit/s and only accepts values from [twai.c's macros](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/peripherals/twai.html)

### `transmit(id: int, ext: bool, rtr: bool, data_or_dlc: Union[str, int])`
Send a packet over the bus.
- If your sending a data packet (`rtr = False`), the last argument is a string containing the data (any character after the 8th will be ignored).
- If your sending a remote packet (`rtr = True`), the last argument is the amount of data to request (max `8`).
Creates a RuntimeError if the bus is too busy.

### `receive() -> tuple`
Receive a packet from the bus and returns the `transmit`'s arguments in a tuple.
Creates a RuntimeError if no message was received.

### `stop()`
Stop the can module

### `on_receive(callback: Callable)`
Set a callback to be called when a packet is received.
This callback gets an argument which is always `None`.*
To get the actual message the callback needs to call `can.receive()` itself.

*(micropython wants exactly one argument in order to make use of its scheduler)
