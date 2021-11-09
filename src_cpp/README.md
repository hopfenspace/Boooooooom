# Boooooooom cpp code

The common Arduino library is used for the ESP32.

## Directory structure
```
src_cpp/
├─ lib/                     --Used for internal libraries
├─ modules/                 --Source for modules
│  ├─ <module_name>/        --Name of the module
│  │  ├─ lib/               --Directory for internal liraries
│  │  ├─ src/               --Directory for main source
│  │  ├─ requirements.json  --Requirements file for internal libs, see init_cpp_module.py
├─ init_cpp_module.py       --Helper script to update and add libs for modules
```

