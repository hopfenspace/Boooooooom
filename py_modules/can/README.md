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

### `set_filter(code: int, mask: int)`
For every bit set to `0` in `mask` an incoming package must match `code`'s bits.
Where `mask` is `1` the `code`'s bits will be ignored.

The layout, which `code` bit corresponds to which package bit,
isn't trivial, so check the [official docs](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/peripherals/twai.html#acceptance-filter).
- Must be called before `start` to take effect.

### `set_pins(tx: int, rx: int)`
Specify the pins to use.
Defaults to 5 and 4.
- Must be called before `start` to take effect.

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
For performance reasons many multiple messages might be bundled together.
So this callback receives a list of messages as argument.
Each message is a tuple of the form

    (id_: int, is_extd: bool, is_request: bool, data_or_size: Union[str, int])

Where `data_or_size` depends on whether the message is a request or not.
