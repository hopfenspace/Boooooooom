use core::fmt::{Display, Formatter};

use esp_twai::message::Identifier;

/// The bomb transmission unit defines a message's sender, recipient and type.
#[derive(Copy, Clone, Eq, PartialEq, Debug, Hash)]
pub struct BombTransmissionUnit {
    /// 3 bits | 4 bits | 4 bits  | 8 bits   | 1 bit | 12 bits
    ///  empty | SND ID | RECV ID | MSG TYPE | EOT   | reserved (by BMP)
    data: u32,
}
impl BombTransmissionUnit {
    /// Get an empty bomb transmission unit
    pub const fn new() -> Self {
        BombTransmissionUnit { data: 0 }
    }

    /// Get the `sender` field
    ///
    /// Only the 4 low bits are actually used
    pub const fn get_sender(&self) -> u8 {
        let snd = self.data & (0b1111 << 25);
        (snd >> 25) as u8
    }

    /// Get the `receiver` field
    ///
    /// Only the 4 low bits are actually used
    pub const fn get_receiver(&self) -> u8 {
        let recv = self.data & (0b1111 << 21);
        (recv >> 21) as u8
    }

    /// Get the `message_type` field
    pub const fn get_message_type(&self) -> u8 {
        let msg_type = self.data & (0b11111111 << 13);
        (msg_type >> 13) as u8
    }

    /// Get the `end_of_transmission` flag
    pub const fn get_end_of_transmission(&self) -> bool {
        let eot = self.data & (1 << 12);
        eot != 0
    }

    /// Set the `sender` field
    ///
    /// Only the 4 low bits are actually used
    pub fn set_sender(&mut self, snd: u8) {
        let snd = (snd as u32 & 0b1111) << 25;
        self.data &= !(0b1111 << 25);
        self.data |= snd;
    }

    /// Set the `receiver` field
    ///
    /// Only the 4 low bits are actually used
    pub fn set_receiver(&mut self, recv: u8) {
        let recv = (recv as u32 & 0b1111) << 21;
        self.data &= !(0b1111 << 21);
        self.data |= recv;
    }

    /// Set the `message_type` field
    pub fn set_message_type(&mut self, msg_type: u8) {
        let msg_type = (msg_type as u32 & 0b11111111) << 13;
        self.data &= !(0b11111111 << 13);
        self.data |= msg_type;
    }

    /// Set the `end_of_transmission` flag
    pub fn set_end_of_transmission(&mut self, eot: bool) {
        let eot = (eot as u32) << 12;
        self.data &= !(0b1 << 12);
        self.data |= eot;
    }
}

impl From<BombTransmissionUnit> for Identifier {
    fn from(btu: BombTransmissionUnit) -> Self {
        Identifier::Extended(btu.data)
    }
}

impl TryFrom<Identifier> for BombTransmissionUnit {
    type Error = NotExtendedFormat;

    fn try_from(value: Identifier) -> Result<Self, Self::Error> {
        match value {
            Identifier::Normal(_) => Err(NotExtendedFormat),
            Identifier::Extended(data) => Ok(BombTransmissionUnit { data }),
        }
    }
}

/// Simple error stating the [Identifier] is not in the extended format.
///
/// Therefore it is not valid for the bomb message protocol.
#[derive(Copy, Clone, Eq, PartialEq, Debug, Hash)]
pub struct NotExtendedFormat;

impl Display for NotExtendedFormat {
    fn fmt(&self, f: &mut Formatter<'_>) -> core::fmt::Result {
        f.write_str("Identifier is not in the extended format.")
    }
}

/// The message types known to Bomb Message Protocol v1
#[derive(Copy, Clone, Eq, PartialEq, Debug, Hash)]
pub enum MessageType {
    /// `0x00` RESET (Master ➜ Slave)
    /// - _Req_: Reset slave modules
    /// - _Data_: **illegal**
    Reset = 0x00,

    /// `0x01` INIT (Master ➜ Slave)
    /// - _Req_: Setup the slave module and trigger manual generation
    /// - _Data_: **illegal**
    Init = 0x01,

    /// `0x02` START (Master ➜ Slave)
    /// - _Req_: Start the game and the slave module’s lifecycle, once for every module
    /// - _Data_: **illegal**
    Start = 0x02,

    /// `0x03` DEFUSED (Master ➜ Slave)
    /// - _Req_: Stop the game and the module's lifecycle, the user won the game
    /// - _Data_: **illegal**
    Defused = 0x03,

    /// `0x04` EXPLODED (Master ➜ Slave)
    /// - _Req_: Stop the game and the module's lifecycle, the user lost the game
    /// - _Data_: **illegal**
    Exploded = 0x04,

    /// `0x05` RTFM (Master ➜ Slave)
    /// - _Req_: Request the transfer of the manual to the master node
    /// - _Data_: HTML in ASCII without `head` or `body` tags, just starting with the content (primary heading level is `h2`)
    RTFM = 0x05,

    /// `0x06` VERSION (Peer ➜ Peer)
    /// - _Req_: Request the version of the `BMP` implementation
    /// - _Data_: Version code of the running `BMP` implementation
    ///     - 1 byte, an unsigned integer (`uint8`), minimal value `0x01`
    Version = 0x06,

    /// `0x07` MODULE_INFO (Peer ➜ Peer)
    /// - _Req_: Request static structured module information from a peer
    /// - _Data_: **TODO: how should this "structured" information look like?**
    ModuleInfo = 0x07,

    /// `0x08` REGISTER (Slave ➜ Master)
    /// - _Req_: Says hello to the master to register itself, but doesn't provide any additional information (the master may ask for those information using `MODULE_INFO`)
    /// - _Data_: **illegal**
    Register = 0x08,

    /// `0x09` STRIKE (Slave ➜ Master)
    /// - _Req_: Adds a single strike
    /// - _Data_: **illegal**
    Strike = 0x09,

    /// `0x0a` DETONATE (Slave ➜ Master)
    /// - _Req_: Immediately trigger the explosion of the bomb, the player looses
    /// - _Data_: **illegal**
    Detonate = 0x0a,

    /// `0x0b` MARK_SOLVED (Slave ➜ Master)
    /// - _Req_: Marks the module as solved (not for unfinished needy modules)
    /// - _Data_: **illegal**
    MarkSolved = 0x0b,

    /// `0x0c` MARK_REACTIVATED (Slave ➜ Master)
    /// - _Req_: Marks the module as re-activated (only valid after `MARK_SOLVED` has been sent in one game session before)
    /// - _Data_: **illegal**
    MarkReactivated = 0x0c,

    /// `0x0d` CHANGE_TIMER (Slave ➜ Master)
    /// - _Req_: **illegal**
    /// - _Data_: Add/subtract the number of 1/10s to/from the timer (depending on the integer's sign)
    ///     - 2 bytes, a signed integer (`int16`)
    ///       :::warning
    ///       Integer overflows may occur in the master here. Fix them correctly.
    ///       :::
    ChangeTimer = 0x0d,

    /// `0x0e` CHANGE_SERIAL_NO (Slave ➜ Master)
    /// - _Req_: Request the master to change the serial number
    /// - _Data_: **illegal**
    ChangeSerialNumber = 0x0e,

    /// `0x0f` TIMER (Slave ➜ Master)
    /// - _Req_: Request the current remaining time in 1/10s
    /// - _Data_: Current remaining time in 1/10s
    ///     - 4 bytes, an unsigned integer (`uint32`)
    Timer = 0x0f,

    /// `0x10` SERIAL_NO (Slave ➜ Master)
    /// - _Req_: Request the current serial number of the bomb
    /// - _Data_: Current serial number
    ///     - 8 bytes, 8 ASCII characters
    SerialNumber = 0x10,

    /// `0x11` STRIKES (Slave ➜ Master)
    /// - _Req_: Request the current number of strikes
    /// - _Data_: Current number of strikes
    ///     - 1 byte, an unsigned int/byte (`uint8`)
    Strikes = 0x11,

    /// `0x12` MAX_STRIKES (Slave ➜ Master)
    /// - _Req_: Request the configured number of maximal strikes before detonation
    /// - _Data_: Configured number of max strikes
    ///     - 1 byte, an unsigned int/byte (`uint8`)
    MaxStrikes = 0x12,

    /// `0x13` MODULE_COUNT (Slave ➜ Master)
    /// - _Req_: Request the number of currently available modules in the whole bomb
    /// - _Data_: Number of available modules
    ///     - 1 byte, an unsigned int/byte (`uint8`)
    ModuleCount = 0x13,

    /// `0x14` ACTIVE_MODULE_COUNT (Slave ➜ Master)
    /// - _Req_: Request the number of currently active (unfinished) modules in the bomb
    /// - _Data_: Number of currently active modules
    ///     - 1 byte, an unsigned int/byte (`uint8`)
    ActiveModuleCount = 0x14,

    /// `0x15` DIFFICULTY (Slave ➜ Master)
    /// - _Req_: Request the current bomb difficulty
    /// - _Data_: Currently configured bomb difficulty
    ///     - 1 byte, an unsigned int/byte (see [Difficulty])
    Difficulty = 0x15,

    /// `0x16` LABELS (Slave ➜ Master)
    /// - _Req_: Request a list of all active and inactive labels on the bomb
    /// - _Data_: Send a list of all labels with its corresponding state in the following format: `{state}{label}`, where state is either `0x00` or `0x01` and label is a three character ASCII encoded string
    Labels = 0x16,

    /// `0x17` BLACKOUT (Master ➜ Slave)
    /// - _Req_: Toggle the _BLACKOUT!_ mode (enables/disables output of the module, input MUST be still allowed)
    /// - _Data_: **illegal**
    Blackout = 0x17,

    /// `0x18` IS_SOLVED (Slave ➜ Slave)
    /// - _Req_: Request the solved state of another slave (not Master)
    /// - _Data_: 1 byte, an unsigned int/byte (`uint8`) as bool (`0x00`: False, `0x01`: True)
    IsSolved = 0x18,

    /// `0x19` SEED (Slave ➜ Master)
    /// - _Req_: Request the current round's seed
    /// - _Data_: Current round's seed
    ///     - 4 bytes, an unsigned integer (`uint32`)
    Seed = 0x19,
}

/// The bomb's difficulty
///
/// Interpreting and implementing different difficulties is module-specific. A module doesn't have to implement difficulties, even though recommended.
#[derive(Copy, Clone, Eq, PartialEq, Debug, Hash)]
pub enum Difficulty {
    /// The same difficulty as `NORMAL`, but things like `DETONATE` or `STRIKE` shouldn't be invoked.
    Immortal = 0,

    /// Training difficulty
    Training = 1,

    /// Easy difficulty
    Easy = 2,

    /// Normal difficulty
    Normal = 3,

    /// Hard difficulty
    Hard = 4,

    /// Expert difficulty
    Expert = 5,

    /// Prepare to die difficulty
    PrepareToDie = 6,
}
