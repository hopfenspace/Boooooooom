#![no_std]
#![no_main]

use esp_twai::message;
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

    let msg = message::Message {
        identifier: message::Identifier::Normal(0),
        data: message::Data::Borrowed("Kuchen?!".as_bytes()),
        single_shot: false,
        self_reception: false,
    };
    if let Err(_) = twai::transmit(&msg.into(), 0) {
        error!("Couldn't push message to transmit");
    }
    info!("Send message");

    match twai::receive(1_000) {
        Ok(msg) => {
            let msg = message::Message::from(msg);
            match core::str::from_utf8(&msg.data) {
                Ok(string) => info!("Received message: \"{}\"", string),
                Err(_) => error!("Couldn't decode message: {:?}", msg.data),
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
