#![no_std]
#![no_main]

use esp_idf_sys as _;

#[no_mangle]
fn main() {
    esp_idf_sys::link_patches();
    esp_idf_svc::log::EspLogger::initialize_default();
}
