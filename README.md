# Esp prototyping repo

## Documentation

`cargo doc` will fail to compile `esp_idf_sys`, because it requires a specific target:

```bash
cargo doc --target riscv32imc-esp-espidf
```

The resulting documentation will be in `target/riscv32imc-esp-espidf/doc` instead of `target/doc`
