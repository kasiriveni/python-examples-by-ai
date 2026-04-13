"""
File reading and writing in Python.
"""
import os
import tempfile

# Create a temp directory for examples
tmp_dir = tempfile.mkdtemp()

# Writing text files
filepath = os.path.join(tmp_dir, "example.txt")
with open(filepath, 'w') as f:
    f.write("Line 1\n")
    f.write("Line 2\n")
    f.writelines(["Line 3\n", "Line 4\n", "Line 5\n"])

# Reading entire file
with open(filepath, 'r') as f:
    content = f.read()
print(f"Full content:\n{content}")

# Reading line by line
with open(filepath, 'r') as f:
    for line_num, line in enumerate(f, 1):
        print(f"Line {line_num}: {line.rstrip()}")

# Reading into a list
with open(filepath, 'r') as f:
    lines = f.readlines()
print(f"\nAs list: {lines}")

# Appending to file
with open(filepath, 'a') as f:
    f.write("Line 6 (appended)\n")

# Reading specific number of characters
with open(filepath, 'r') as f:
    chunk = f.read(20)
    print(f"\nFirst 20 chars: {chunk!r}")
    rest = f.read()
    print(f"Rest: {rest!r}")

# Writing binary files
bin_path = os.path.join(tmp_dir, "data.bin")
with open(bin_path, 'wb') as f:
    f.write(b'\x00\x01\x02\x03\x04')

with open(bin_path, 'rb') as f:
    data = f.read()
print(f"\nBinary data: {data}")

# File modes summary
modes = {
    'r': 'Read text (default)',
    'w': 'Write text (truncates)',
    'a': 'Append text',
    'x': 'Exclusive create (fails if exists)',
    'rb': 'Read binary',
    'wb': 'Write binary',
    'r+': 'Read and write',
}
print("\nFile modes:")
for mode, desc in modes.items():
    print(f"  '{mode}': {desc}")

# Cleanup
import shutil
shutil.rmtree(tmp_dir)
print("\nTemp files cleaned up.")
