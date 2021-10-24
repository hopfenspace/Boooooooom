CAN_MOD_DIR := $(USERMOD_DIR)

# Add all C files to SRC_USERMOD.
SRC_USERMOD += $(CAN_MOD_DIR)/can.c

# We can add our module folder to include paths if needed
# This is not actually needed in this example.
CFLAGS_USERMOD += -I$(CAN_MOD_DIR)
CAN_MOD_DIR := $(USERMOD_DIR)
