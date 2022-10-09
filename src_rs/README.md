# RUUUUUUUUMMST

BOOOOOOOOM but rust <3

## Install toolchain

We used [espup](https://github.com/esp-rs/espup) to install the esp toolchain:

```
cargo install espup --git https://github.com/esp-rs/espup
```

```
espup install
```

Remember to run before compiling:

```bash
source export-esp.sh
```

## Documentation

`cargo doc` will fail to compile `esp_idf_sys`, because it requires a specific target:

```bash
cargo doc --target riscv32imc-esp-espidf
```

The resulting documentation will be in `target/riscv32imc-esp-espidf/doc` instead of `target/doc`
