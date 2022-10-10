//! Bomb Message Protocol
#![no_std]
#![warn(missing_docs)]

/// Implementation of the BombTransmissionUnit
pub mod btu;

use esp_idf_sys::{gpio_num_t, twai_timing_config_t};
use esp_twai::twai::{
    default_config, install, start, stop, uninstall, FILTER_ACCEPT_ALL, NORMAL_MODE,
};
use log::error;

/**
Timings for the TWAI driver exported from `esp-twai`.
*/
pub use esp_twai::twai::{
    TIMING_100KBITS, TIMING_10KBITS, TIMING_125KBITS, TIMING_12_5KBITS, TIMING_16KBITS,
    TIMING_1KBITS, TIMING_1MBITS, TIMING_20KBITS, TIMING_250KBITS, TIMING_25KBITS, TIMING_500KBITS,
    TIMING_50KBITS, TIMING_5KBITS, TIMING_800KBITS,
};

// --------
// Common
// --------

/// Helper struct for the exact same methods in [Master] and [Slave].
struct Common;
impl Common {
    fn begin(&self, tx_pin: gpio_num_t, rx_pin: gpio_num_t, timing: &twai_timing_config_t) -> bool {
        stop();
        uninstall();

        if let Err(e) = install(
            &default_config(tx_pin, rx_pin, NORMAL_MODE),
            timing,
            &FILTER_ACCEPT_ALL,
        ) {
            error!("{:?}", e);
            return false;
        }

        start()
    }
}

// --------
// Master
// --------

/**
Implementation of a Master.
*/
pub struct Master {
    common: Common,
}

impl Master {
    /**
    Returns a new instance of a master.
    */
    pub fn new() -> Self {
        Self { common: Common }
    }

    /**
    Starts the underlying TWAI driver.

    Stops and uninstalls any previous installed driver.

    **Parameter**:
    - `tx_pin`: TX pin for the TWAI module.
    - `rx_pin`: RX pin for the TWAI module.
    - `timing`: Timing the TWAI module should use. Some timings are re-exported from `esp-twai`.

    Returns false if anything went wrong.
     */
    pub fn begin(
        &self,
        tx_pin: gpio_num_t,
        rx_pin: gpio_num_t,
        timing: &twai_timing_config_t,
    ) -> bool {
        self.common.begin(tx_pin, rx_pin, timing)
    }
}

// --------
// Slave
// --------

/**
Implementation of a slave device.
*/
pub struct Slave {
    common: Common,
    address: u8,
}

impl Slave {
    /**
    Create a new instance of a slave.

    If None is returned, address == 0 || address > 15
    */
    pub fn new(address: u8) -> Option<Self> {
        if address == 0 || address > 15 {
            return None;
        }
        Some(Self {
            common: Common,
            address,
        })
    }

    /**
    Starts the underlying TWAI driver.

    Stops and uninstalls any previous installed driver.

    **Parameter**:
    - `tx_pin`: TX pin for the TWAI module.
    - `rx_pin`: RX pin for the TWAI module.
    - `timing`: Timing the TWAI module should use. Some timings are re-exported from `esp-twai`.

    Returns false if anything went wrong.
    */
    pub fn begin(
        &self,
        tx_pin: gpio_num_t,
        rx_pin: gpio_num_t,
        timing: &twai_timing_config_t,
    ) -> bool {
        self.common.begin(tx_pin, rx_pin, timing)
    }
}
