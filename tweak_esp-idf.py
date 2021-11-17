#!/usr/bin/evn python3

import sys, os
base_dir = os.path.join(sys.argv[1], "components", "driver")
header_file = os.path.join(base_dir, "include", "driver", "twai.h")
c_file = os.path.join(base_dir, "twai.c")

# Read
with open(header_file) as f:
    header = f.read()
with open(c_file) as f:
    c = f.read()

# Modify
if "void set_handler_extension(intr_handler_t handler);" in header:
    print("skipping header")
else:
    after = "/* ------------------------------ Public API -------------------------------- */\n"
    index = header.find(after) + len(after) + 1
    header = header[:index] + "void set_handler_extension(intr_handler_t handler);\n\n" + header[index:]
if "static intr_handler_t handler_extension = NULL;" in c:
    print("skipping c")
else:
    after = "/* -------------------- Interrupt and Alert Handlers ------------------------ */\n"
    index = c.find(after) + len(after) + 1
    c = c[:index] + "static intr_handler_t handler_extension = NULL;\n\n" + c[index:]

    after = "/* ---------------------------- Public Functions ---------------------------- */\n"
    index = c.find(after) + len(after) + 1
    c = c[:index] + """void set_handler_extension(intr_handler_t handler) {
    handler_extension = handler;
}

""" + c[index:]

    after = """if (task_woken == pdTRUE) {
        portYIELD_FROM_ISR();
    }"""
    index = c.find(after) + len(after) + 1
    c = c[:index] + """
    if (handler_extension != NULL) {
        handler_extension(&events);
    }
""" + c[index:]

# Write
with open(header_file, "w") as f:
    f.write(header)
with open(c_file, "w") as f:
    f.write(c)
