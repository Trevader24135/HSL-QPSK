import numpy as np

_POLY = np.array([1, 1, 0, 0, 1, 1, 0, 1, 1], dtype=np.uint8) # 0x9B

def crc8(data: bytes, check: int = None) -> int:
    if check is not None:
        padding = check.to_bytes()
    else:
        padding = b'\x00'

    np_bytes = np.frombuffer(data + padding, dtype=np.uint8)
    data_bits = np.unpackbits(np_bytes)

    for i in range(0, data_bits.size - 8):
        if data_bits[i] == 1:
            data_bits[i:i+9] = np.bitwise_xor(_POLY, data_bits[i:i+9])

    return int(np.packbits(data_bits[-8:])[0])

if __name__ == "__main__":
    _data = b"testing!"
    _crc = crc8(_data)
    assert crc8(_data, _crc) == 0
