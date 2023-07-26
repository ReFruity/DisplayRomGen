def is_bit_set(byte: int, bit_address: int) -> bool:
    return (byte >> bit_address) % 2 == 1
