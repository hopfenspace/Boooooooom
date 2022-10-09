//! Bomb Message Protocol
#![no_std]
#![warn(missing_docs)]

/// The message types known to Bomb Message Protocol v1
#[derive(Copy, Clone, Eq, PartialEq, Debug, Hash)]
pub enum MessageType {
    /// `0x01` INIT (Master ➜ Slave)
    /// - _Req_: Setup the slave module and trigger manual generation
    /// - _Data_: **illegal**
    Reset = 0x00,

    /// `0x02` START (Master ➜ Slave)
    /// - _Req_: Start the game and the slave module’s lifecycle, once for every module
    /// - _Data_: **illegal**
    Init = 0x01,

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
