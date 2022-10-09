//! Provides high level structs and enums for messages.

use core::ops::Deref;

use esp_idf_sys::{
    twai_message_t, twai_message_t__bindgen_ty_1, twai_message_t__bindgen_ty_1__bindgen_ty_1,
};

/// A message's identifier is an 11bit or 29bit number depending on the frame format.
///
/// It is used to prioritize different messages during the arbitration. Lower values are of higher priority.
#[derive(Copy, Clone, Debug)]
pub enum Identifier {
    /// Use the normal 11 bit format
    ///
    /// The 21 high bits will be discarded
    Normal(u32),

    /// Use the extended 29 bit format
    ///
    /// The 3 high bits will be discarded
    Extended(u32),
}
impl Deref for Identifier {
    type Target = u32;

    fn deref(&self) -> &Self::Target {
        match self {
            Identifier::Normal(id) => id,
            Identifier::Extended(id) => id,
        }
    }
}

/// A message's data consists of 0 to 8 bytes.
///
/// When sending a remote request, the data will always be empty.
/// A remote request is a request for data from another node on the bus.
///
/// When constructing a [Message] for transmission, it can be provided as array or slice.
#[derive(Copy, Clone, Debug)]
pub enum Data<'data> {
    /// Request data instead of sending some
    RemoteRequest,

    /// Transmit data from a slice
    Borrowed(&'data [u8]),

    /// Transmit or receive data as array
    Owned {
        /// How many bytes (max 8) of data are to be considered set.
        length: usize,
        /// Data, use length when not all bytes are to be considered set.
        data: [u8; 8],
    },
}
impl<'data> Deref for Data<'data> {
    type Target = [u8];

    fn deref(&self) -> &Self::Target {
        match self {
            Data::RemoteRequest => &[],
            Data::Borrowed(slice) => slice,
            Data::Owned { data, length } => &data[0..*length],
        }
    }
}

// TODO: add TWAI_MSG_FLAG_DLC_NON_COMP flag
/// A high-level struct representing sendable and receivable messages.
///
/// It can be converted from and into a [twai_message_t].
#[derive(Copy, Clone, Debug)]
pub struct Message<'data> {
    /// The message's identifier
    pub identifier: Identifier,

    /// The message's data
    pub data: Data<'data>,

    /// Transmit message using Single Shot Transmission
    ///
    /// i.e.: Message will not be retransmitted upon error or loss of arbitration.
    pub single_shot: bool,

    /// Transmit message using Self Reception Request
    ///
    /// i.e.: Transmitted message will also received by the same node.
    pub self_reception: bool,
}

impl<'data> From<Message<'data>> for twai_message_t {
    fn from(msg: Message) -> Self {
        let mut flags = twai_message_t__bindgen_ty_1__bindgen_ty_1::default();
        flags.set_ss(msg.single_shot as u32);
        flags.set_self(msg.self_reception as u32);

        let identifier = match msg.identifier {
            Identifier::Normal(id) => {
                flags.set_extd(0);
                id
            }
            Identifier::Extended(id) => {
                flags.set_extd(1);
                id
            }
        };

        let mut data = [0u8; 8];
        let mut length = 0;
        match msg.data {
            Data::RemoteRequest => flags.set_rtr(1),
            Data::Borrowed(slice) => {
                length = slice.len().max(8);
                (&mut data[0..length]).copy_from_slice(&slice[0..length]);
                flags.set_rtr(0);
            }
            Data::Owned {
                length: msg_length,
                data: msg_data,
            } => {
                length = msg_length.max(8);
                data = msg_data;
                flags.set_rtr(0);
            }
        }

        twai_message_t {
            __bindgen_anon_1: twai_message_t__bindgen_ty_1 {
                __bindgen_anon_1: flags,
            },
            identifier,
            data_length_code: length as u8,
            data,
        }
    }
}

impl From<twai_message_t> for Message<'static> {
    fn from(msg: twai_message_t) -> Self {
        let twai_message_t {
            identifier,
            data,
            data_length_code: length,
            __bindgen_anon_1,
        } = msg;
        let flags = unsafe { __bindgen_anon_1.__bindgen_anon_1 };

        let identifier = if flags.extd() != 0 {
            Identifier::Extended(identifier)
        } else {
            Identifier::Normal(identifier)
        };

        let data = if flags.rtr() != 0 {
            Data::RemoteRequest
        } else {
            Data::Owned {
                length: length as usize,
                data,
            }
        };

        Message {
            identifier,
            data,
            single_shot: flags.ss() != 0,
            self_reception: flags.self_() != 0,
        }
    }
}
