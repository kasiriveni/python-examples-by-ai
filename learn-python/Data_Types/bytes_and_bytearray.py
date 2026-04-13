"""
Bytes, Bytearray, and Memoryview in Python.
"""

# Bytes (immutable)
b1 = b"hello"
b2 = bytes([72, 101, 108, 108, 111])
b3 = bytes.fromhex("48656c6c6f")
print(f"b1: {b1}, b2: {b2}, b3: {b3}")
print(f"All equal: {b1 == b2 == b3}")

# Encoding and decoding
text = "Hello, World! 🌍"
encoded = text.encode("utf-8")
decoded = encoded.decode("utf-8")
print(f"Encoded: {encoded}")
print(f"Decoded: {decoded}")

# Bytearray (mutable)
ba = bytearray(b"hello")
ba[0] = 72  # 'H'
ba.append(33)  # '!'
ba.extend(b" world")
print(f"Bytearray: {ba}")
print(f"As string: {ba.decode()}")

# Memoryview (zero-copy slicing)
data = bytearray(b"Hello, World!")
mv = memoryview(data)
slice_view = mv[7:12]
print(f"Memoryview slice: {bytes(slice_view)}")

# Modify through memoryview
slice_view[0:5] = b"Earth"
print(f"Modified through memoryview: {data}")

# Hex conversions
data = b"Python"
print(f"To hex: {data.hex()}")
print(f"From hex: {bytes.fromhex(data.hex())}")

# Struct for binary data
import struct
packed = struct.pack('>I H', 65535, 256)
print(f"Packed: {packed}")
unpacked = struct.unpack('>I H', packed)
print(f"Unpacked: {unpacked}")
