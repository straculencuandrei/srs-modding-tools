import os
import struct

exe_path = os.path.join("..", "Bin", "SRS.EXE")

with open(exe_path, "rb") as f:
    data = f.read()

# Address of MP2PCLoadGameState string reference
ref_offset = 0x24E5
start = max(0, ref_offset - 0x60)
end = min(len(data), ref_offset + 0x20)

chunk = data[start:end]
print("Hex dump backwards from MP2PCLoadGameState string reference:")
for i in range(0, len(chunk), 16):
    row = chunk[i:i+16]
    hex_str = " ".join(f"{b:02X}" for b in row)
    print(f"0x{start+i:08X}: {hex_str}")

# Look for standard prologue like `56 8B F1` or `55 8B EC`
