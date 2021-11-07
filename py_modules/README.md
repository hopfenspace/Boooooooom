# Custom Micropython

This directory contains custom c modules for micropython.

## Initial setup

(Mostly based on [micropython's instructions](https://github.com/micropython/micropython/tree/master/ports/esp32#readme))

Get the esp-idf for building the esp32 port:

`git clone -b v4.2 --recursive https://github.com/espressif/esp-idf.git`

Go into the esp-idf repo and install it:

`./install.sh`

Go to the micropython repo and compile the cross-compiler:

`make -C mpy-cross`

Go to into `ports/esp32` in micropython's repo and get dependencies:

`make submodules`

To flash the esp you need the OS permission:

`sudo adduser <username> dialout`

or for Arch-Linux:
`sudo useradd -a -G uucp <username>`

**Finally apply some tweaks to esp-idf's code in order to compile some of our custom modules.
This directory contains a `tweak_esp-idf.py` script. Execute it with the path to your esp-idf repo as argument.**

Building might fail due to some certificate error.
To fix this you have to try compiling once, so the build directoy gets created.
Edit the `build-GENERIC/sdkconfig` file in `ports/esp32`. There unset `CONFIG_MBEDTLS_CERTIFICATE_BUNDLE_DEFAULT_FULL`
and set `CONFIG_MBEDTLS_CERTIFICATE_BUNDLE_DEFAULT_CMN`.

## How to compile

Enter esp-idf's build environment by calling:

`source export.sh`

(The `fish` version didn't work for me, so I always used `bash` for compiling)

Now just go to micropython's `ports/esp32` and compile with the custom module:

`make USER_C_MODULES=<path to this repo>/py_modules/can/micropython.cmake`

To flash the binary, use:

`make erase` (if necessary) and `make deploy`
