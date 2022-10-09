#![no_std]
#![no_main]

use esp_twai::twai;

use esp_idf_sys as _; // If using the `binstart` feature of `esp-idf-sys`, always keep this module imported

use log::*;

#[no_mangle]
fn main() {
    // Temporary. Will disappear once ESP-IDF 4.4 is released, but for now it is necessary to call this function once,
    // or else some patches to the runtime implemented by esp-idf-sys might not link properly.
    esp_idf_sys::link_patches();

    // Bind the log crate to the ESP Logging facilities
    esp_idf_svc::log::EspLogger::initialize_default();

    if let Err(error) = twai::install(
        &twai::default_config(5, 4, twai::NORMAL_MODE),
        &twai::TIMING_1MBITS,
        &twai::FILTER_ACCEPT_ALL,
    ) {
        error!("Couldn't install driver: {:?}", error);
    }
    if !twai::start() {
        error!("Couldn't start driver");
    }
    info!("TWAI started");

    let mut message = esp_idf_sys::twai_message_t::default();
    message.data_length_code = 8;
    message.data.copy_from_slice("Kuchen?!".as_bytes());
    if let Err(_) = twai::transmit(&message, 0) {
        error!("Couldn't push message to transmit");
    }
    info!("Send message");

    match twai::receive(1_000) {
        Ok(message) => {
            let length = message.data_length_code.max(8) as usize;
            let data = &message.data[0..length];
            match core::str::from_utf8(data) {
                Ok(string) => info!("Received message: \"{}\"", string),
                Err(_) => error!("Couldn't decode message: {:?}", data),
            }
        }
        Err(_) => error!("Couldn't receive message"),
    }

    if !twai::stop() {
        error!("Couldn't stop driver");
    }
    if !twai::uninstall() {
        error!("Couldn't uninstall driver");
    }
    info!("TWAI stoped");
}
