import re
import numpy as np
from pathlib import Path

header_file = Path("animation.h")

with header_file.open("r", encoding="utf-8", errors="ignore") as f:
    data = f.read()

pattern = re.compile(r'cat_frames\[.*?\]\s*=\s*\{(.*?)\};', re.S)
match = pattern.search(data)
if not match:
    raise ValueError("Could not find cat_frames array in the header")

hex_bytes = re.findall(r'0x[0-9A-Fa-f]{2}', match.group(1))
byte_values = np.array([int(h, 16) for h in hex_bytes], dtype=np.uint8)

frame_size = 512
frame_count = len(byte_values) // frame_size
frames = byte_values.reshape((frame_count, frame_size))

bin_file = header_file.with_name("cat.bin")
frames.tofile(bin_file)
print(f"Created SD binary: {bin_file} ({frame_count} frames, {frame_size} bytes each)")