//! Maps [esp_err_t] into an [enum]
//!
//! https://github.com/espressif/esp-idf/blob/master/components/esp_common/include/esp_err.h
//!
//! [enum]: EspError
use core::ffi::CStr;
use core::fmt;

use esp_idf_sys::{
    esp_err_t, esp_err_to_name, ESP_ERR_INVALID_ARG, ESP_ERR_INVALID_CRC, ESP_ERR_INVALID_MAC,
    ESP_ERR_INVALID_RESPONSE, ESP_ERR_INVALID_SIZE, ESP_ERR_INVALID_STATE, ESP_ERR_INVALID_VERSION,
    ESP_ERR_NOT_FINISHED, ESP_ERR_NOT_FOUND, ESP_ERR_NOT_SUPPORTED, ESP_ERR_NO_MEM,
    ESP_ERR_TIMEOUT, ESP_FAIL, ESP_OK,
};

/// An error code returned by esp-idf
#[derive(Copy, Clone, Debug, Eq, PartialEq, Hash)]
pub enum EspError {
    /// Generic error
    Fail = ESP_FAIL as isize,

    /// Out of Memory
    OutOfMemory = ESP_ERR_NO_MEM as isize,

    /// Invalid Argument
    InvalidArgument = ESP_ERR_INVALID_ARG as isize,

    /// Invalid State
    InvalidState = ESP_ERR_INVALID_STATE as isize,

    /// Invalid Size
    InvalidSize = ESP_ERR_INVALID_SIZE as isize,

    /// Requested resource not found
    NotFound = ESP_ERR_NOT_FOUND as isize,

    /// Operation or feature not supported
    NotSupported = ESP_ERR_NOT_SUPPORTED as isize,

    /// Operation timed out
    Timeout = ESP_ERR_TIMEOUT as isize,

    /// Received response was invalid
    InvalidResponse = ESP_ERR_INVALID_RESPONSE as isize,

    /// CRC or checksum was invalid
    InvalidCRC = ESP_ERR_INVALID_CRC as isize,

    /// Version was invalid
    InvalidVersion = ESP_ERR_INVALID_VERSION as isize,

    /// MAC address was invalid
    InvalidMAC = ESP_ERR_INVALID_MAC as isize,

    /// There are items remained to retrieve
    NotFinished = ESP_ERR_NOT_FINISHED as isize,

    /// An undocumented error code
    Unknown,
}

impl EspError {
    /// Convert an error code into a result.
    ///
    /// Use [Result::map] to give it a value or [Result::map_err] change the error type.
    pub fn convert(code: esp_err_t) -> Result<(), Self> {
        match code {
            ESP_OK => Ok(()),
            ESP_FAIL => Err(EspError::Fail),
            ESP_ERR_NO_MEM => Err(EspError::OutOfMemory),
            ESP_ERR_INVALID_ARG => Err(EspError::InvalidArgument),
            ESP_ERR_INVALID_STATE => Err(EspError::InvalidState),
            ESP_ERR_INVALID_SIZE => Err(EspError::InvalidSize),
            ESP_ERR_NOT_FOUND => Err(EspError::NotFound),
            ESP_ERR_NOT_SUPPORTED => Err(EspError::NotSupported),
            ESP_ERR_TIMEOUT => Err(EspError::Timeout),
            ESP_ERR_INVALID_RESPONSE => Err(EspError::InvalidResponse),
            ESP_ERR_INVALID_CRC => Err(EspError::InvalidCRC),
            ESP_ERR_INVALID_VERSION => Err(EspError::InvalidVersion),
            ESP_ERR_INVALID_MAC => Err(EspError::InvalidMAC),
            ESP_ERR_NOT_FINISHED => Err(EspError::NotFinished),
            _ => Err(EspError::Unknown),
        }
    }
}
impl fmt::Display for EspError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let cstr = unsafe {
            let ptr = esp_err_to_name(*self as esp_err_t);
            CStr::from_ptr(ptr)
        };
        let string = cstr.to_str().map_err(|_| fmt::Error)?;
        f.write_str(string)
    }
}
