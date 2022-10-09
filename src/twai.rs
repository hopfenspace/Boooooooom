use esp_idf_sys::c_types::c_int;
use esp_idf_sys::{
    gpio_num_t, twai_clear_receive_queue, twai_clear_transmit_queue, twai_driver_install,
    twai_driver_uninstall, twai_filter_config_t, twai_general_config_t, twai_get_status_info,
    twai_initiate_recovery, twai_message_t, twai_mode_t, twai_mode_t_TWAI_MODE_NORMAL,
    twai_read_alerts, twai_receive, twai_reconfigure_alerts, twai_start, twai_state_t,
    twai_state_t_TWAI_STATE_BUS_OFF, twai_state_t_TWAI_STATE_RECOVERING,
    twai_state_t_TWAI_STATE_RUNNING, twai_state_t_TWAI_STATE_STOPPED, twai_status_info_t,
    twai_stop, twai_timing_config_t, twai_transmit, TickType_t, ESP_INTR_FLAG_LEVEL1,
    TWAI_ALERT_NONE,
};

use crate::error::EspError;

#[derive(Copy, Clone, Debug)]
pub enum State {
    /// Stopped state. The TWAI controller will not participate in any TWAI bus activities
    Stopped,
    /// Running state. The TWAI controller can transmit and receive messages
    Running,
    /// Bus-off state. The TWAI controller cannot participate in bus activities until it has recovered
    BusOff,
    /// Recovering state. The TWAI controller is undergoing bus recovery
    Recovering,
}
impl From<twai_state_t> for State {
    fn from(state: twai_state_t) -> Self {
        #[allow(non_upper_case_globals)]
        match state {
            twai_state_t_TWAI_STATE_STOPPED => State::Stopped,
            twai_state_t_TWAI_STATE_RUNNING => State::Running,
            twai_state_t_TWAI_STATE_BUS_OFF => State::BusOff,
            twai_state_t_TWAI_STATE_RECOVERING => State::Recovering,
            _ => unreachable!("All possible values should be handled"),
        }
    }
}

/// Copied from twai.h
const TWAI_IO_UNUSED: gpio_num_t = -1;

pub const TIMING_1KBITS: twai_timing_config_t = twai_timing_config_t {
    brp: 4000,
    tseg_1: 15,
    tseg_2: 4,
    sjw: 3,
    triple_sampling: false,
};
pub const TIMING_5KBITS: twai_timing_config_t = twai_timing_config_t {
    brp: 800,
    tseg_1: 15,
    tseg_2: 4,
    sjw: 3,
    triple_sampling: false,
};
pub const TIMING_10KBITS: twai_timing_config_t = twai_timing_config_t {
    brp: 400,
    tseg_1: 15,
    tseg_2: 4,
    sjw: 3,
    triple_sampling: false,
};
pub const TIMING_12_5KBITS: twai_timing_config_t = twai_timing_config_t {
    brp: 256,
    tseg_1: 16,
    tseg_2: 8,
    sjw: 3,
    triple_sampling: false,
};
pub const TIMING_16KBITS: twai_timing_config_t = twai_timing_config_t {
    brp: 200,
    tseg_1: 16,
    tseg_2: 8,
    sjw: 3,
    triple_sampling: false,
};
pub const TIMING_20KBITS: twai_timing_config_t = twai_timing_config_t {
    brp: 200,
    tseg_1: 15,
    tseg_2: 4,
    sjw: 3,
    triple_sampling: false,
};
pub const TIMING_25KBITS: twai_timing_config_t = twai_timing_config_t {
    brp: 128,
    tseg_1: 16,
    tseg_2: 8,
    sjw: 3,
    triple_sampling: false,
};
pub const TIMING_50KBITS: twai_timing_config_t = twai_timing_config_t {
    brp: 80,
    tseg_1: 15,
    tseg_2: 4,
    sjw: 3,
    triple_sampling: false,
};
pub const TIMING_100KBITS: twai_timing_config_t = twai_timing_config_t {
    brp: 40,
    tseg_1: 15,
    tseg_2: 4,
    sjw: 3,
    triple_sampling: false,
};
pub const TIMING_125KBITS: twai_timing_config_t = twai_timing_config_t {
    brp: 32,
    tseg_1: 15,
    tseg_2: 4,
    sjw: 3,
    triple_sampling: false,
};
pub const TIMING_250KBITS: twai_timing_config_t = twai_timing_config_t {
    brp: 16,
    tseg_1: 15,
    tseg_2: 4,
    sjw: 3,
    triple_sampling: false,
};
pub const TIMING_500KBITS: twai_timing_config_t = twai_timing_config_t {
    brp: 8,
    tseg_1: 15,
    tseg_2: 4,
    sjw: 3,
    triple_sampling: false,
};
pub const TIMING_800KBITS: twai_timing_config_t = twai_timing_config_t {
    brp: 4,
    tseg_1: 16,
    tseg_2: 8,
    sjw: 3,
    triple_sampling: false,
};
pub const TIMING_1MBITS: twai_timing_config_t = twai_timing_config_t {
    brp: 4,
    tseg_1: 15,
    tseg_2: 4,
    sjw: 3,
    triple_sampling: false,
};

pub const FILTER_ACCEPT_ALL: twai_filter_config_t = twai_filter_config_t {
    acceptance_code: 0,
    acceptance_mask: 0xFFFFFFFF,
    single_filter: true,
};

pub const NORMAL_MODE: twai_mode_t = twai_mode_t_TWAI_MODE_NORMAL;

/// Get the minimal required config to install the TWAI driver.
pub fn default_config(
    tx_io: gpio_num_t,
    rx_io: gpio_num_t,
    mode: twai_mode_t,
) -> twai_general_config_t {
    twai_general_config_t {
        mode,
        tx_io,
        rx_io,
        clkout_io: TWAI_IO_UNUSED,
        bus_off_io: TWAI_IO_UNUSED,
        tx_queue_len: 5,
        rx_queue_len: 5,
        alerts_enabled: TWAI_ALERT_NONE,
        clkout_divider: 0,
        intr_flags: ESP_INTR_FLAG_LEVEL1 as c_int,
    }
}

/// Error occurring when installing the TWAI driver
#[derive(Copy, Clone, Debug)]
pub enum InstallError {
    /// Driver is already installed
    AlreadyInstalled,
    /// Insufficient memory
    OutOfMemory,
    /// Arguments are invalid
    InvalidArgument,
}

/// Install TWAI driver.
///
/// This function installs the TWAI driver using three configuration structures.
/// The required memory is allocated and the TWAI driver is placed in the stopped state after running this function.
pub fn install(
    general: &twai_general_config_t,
    timing: &twai_timing_config_t,
    filter: &twai_filter_config_t,
) -> Result<(), InstallError> {
    let code =
        unsafe { twai_driver_install(general as *const _, timing as *const _, filter as *const _) };
    let result = EspError::convert(code);
    result.map_err(|error| match error {
        EspError::InvalidArgument => InstallError::InvalidArgument,
        EspError::InvalidState => InstallError::AlreadyInstalled,
        EspError::OutOfMemory => InstallError::OutOfMemory,
        _ => unreachable!("All possible return codes should be handled"),
    })
}

/// Start the TWAI driver.
///
/// This function starts the TWAI driver, putting the TWAI driver into the running state.
/// This allows the TWAI driver to participate in TWAI bus activities such as transmitting/receiving messages.
/// The TX and RX queue are reset in this function, clearing any messages that are unread or pending transmission.
///
/// This function can only be called when the TWAI driver is in the stopped state.
pub fn start() -> bool {
    unsafe { EspError::convert(twai_start()).is_ok() }
}

/// Get current status information of the TWAI driver.
pub fn get_status() -> Option<twai_status_info_t> {
    let mut status = twai_status_info_t::default();
    let code = unsafe { twai_get_status_info(&mut status as *mut _) };
    let result = EspError::convert(code);
    result.map(|_| status).ok()
}

/// Error occurring when scheduling a message to [transmit]
#[derive(Copy, Clone, Debug)]
pub enum TransmitError {
    /// Timed out waiting for space on TX queue
    Timeout,
    /// TX queue is disabled and another message is currently transmitting
    Busy,
    /// TWAI driver is not in running state, or is not installed
    NotRunning,
    /// TWAI driver is in Listen Only Mode which does not support transmissions
    NotSupported,
    /// The message's data length code is larger than the maximum
    TooMuchData,
}

/// Transmit a TWAI message.
///
/// This function queues a TWAI message for transmission.
/// Transmission will start immediately if no other messages are queued for transmission.
/// If the TX queue is full, this function will block until more space becomes available or until it times out.
/// If the TX queue is disabled (TX queue length = 0 in configuration), this function will return immediately if another message is undergoing transmission.
///
/// This function can only be called when the TWAI driver is in the running state and cannot be called under Listen Only Mode.
pub fn transmit(message: &twai_message_t, ticks_to_wait: TickType_t) -> Result<(), TransmitError> {
    let code = unsafe { twai_transmit(message as *const _, ticks_to_wait) };
    let result = EspError::convert(code);
    result.map_err(|error| match error {
        EspError::InvalidArgument => TransmitError::TooMuchData,
        EspError::InvalidState => TransmitError::NotRunning,
        EspError::NotSupported => TransmitError::NotSupported,
        EspError::Timeout => TransmitError::Timeout,
        EspError::Fail => TransmitError::Busy,
        _ => unreachable!("All possible return codes should be handled"),
    })
}

/// Error occurring when performing a blocking read:
/// - [`receive`]
/// - [`read_alerts`]
#[derive(Copy, Clone, Debug)]
pub enum ReadError {
    /// Timed out waiting
    Timeout,
    /// TWAI driver is not installed
    NotInstalled,
}

/// Receive a TWAI message.
///
/// This function receives a message from the RX queue.
/// The flags field of the message structure will indicate the type of message received.
/// This function will block if there are no messages in the RX queue
pub fn receive(ticks_to_wait: TickType_t) -> Result<twai_message_t, ReadError> {
    let mut message = twai_message_t::default();
    let code = unsafe { twai_receive(&mut message as *mut _, ticks_to_wait) };
    let result = EspError::convert(code);
    result.map(|_| message).map_err(|error| match error {
        EspError::InvalidState => ReadError::NotInstalled,
        EspError::Timeout => ReadError::Timeout,
        EspError::InvalidArgument => {
            unreachable!("The pointer to the stack variable shouldn't be null")
        }
        _ => unreachable!("All possible return codes should be handled"),
    })
}

/// Stop the TWAI driver.
///
/// This function stops the TWAI driver, preventing any further message from being transmitted or received until twai_start() is called.
/// Any messages in the TX queue are cleared.
/// Any messages in the RX queue should be read by the application after this function is called.
///
/// This function can only be called when the TWAI driver is in the running state.
pub fn stop() -> bool {
    unsafe { EspError::convert(twai_stop()).is_ok() }
}

/// Uninstall the TWAI driver.
///
/// This function uninstalls the TWAI driver, freeing the memory utilized by the driver.
///
/// This function can only be called when the driver is in the stopped state or the bus-off state.
pub fn uninstall() -> bool {
    unsafe { EspError::convert(twai_driver_uninstall()).is_ok() }
}

/// Start the bus recovery process.
///
/// This function initiates the bus recovery process when the TWAI driver is in the bus-off state.
/// Once initiated, the TWAI driver will enter the recovering state and wait for 128 occurrences of the bus-free signal on the TWAI bus before returning to the stopped state.
/// This function will reset the TX queue, clearing any messages pending transmission.
///
/// This function can only be called when the driver is in the bus-off state.
pub fn initiate_recovery() -> bool {
    unsafe { EspError::convert(twai_initiate_recovery()).is_ok() }
}

/// Read TWAI driver alerts.
///
/// This function will read the alerts raised by the TWAI driver.
/// If no alert has been issued when this function is called, this function will block until an alert occurs or until it timeouts.
pub fn read_alerts(ticks_to_wait: TickType_t) -> Result<u32, ReadError> {
    let mut alerts = 0;
    let code = unsafe { twai_read_alerts(&mut alerts as *mut _, ticks_to_wait) };
    let result = EspError::convert(code);
    result.map(|_| alerts).map_err(|error| match error {
        EspError::InvalidState => ReadError::NotInstalled,
        EspError::Timeout => ReadError::Timeout,
        EspError::InvalidArgument => {
            unreachable!("The pointer to the stack variable shouldn't be null")
        }
        _ => unreachable!("All possible return codes should be handled"),
    })
}

/// Reconfigure which alerts are enabled.
///
/// This function reconfigures which alerts are enabled.
/// If there are alerts which have not been read whilst reconfiguring, this function can read those alerts.
pub fn reconfigure_alerts(alerts_enabled: u32) -> Result<u32, ()> {
    let mut alerts = 0;
    let code = unsafe { twai_reconfigure_alerts(alerts_enabled, &mut alerts as *mut _) };
    let result = EspError::convert(code);
    result.map(|_| alerts).map_err(|error| match error {
        EspError::InvalidState => (),
        _ => unreachable!("All possible return codes should be handled"),
    })
}

/// Clear the transmit queue.
///
/// This function will clear the transmit queue of all messages.
pub fn clear_transmit_queue() -> bool {
    unsafe { EspError::convert(twai_clear_transmit_queue()).is_ok() }
}

/// Clear the receive queue.
///
/// This function will clear the receive queue of all messages.
pub fn clear_receive_queue() -> bool {
    unsafe { EspError::convert(twai_clear_receive_queue()).is_ok() }
}
