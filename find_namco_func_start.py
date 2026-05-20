import os
import struct

exe_path = os.path.join("..", "Bin", "SRS.EXE")
PE_BASE = 0x00400000

with open(exe_path, "rb") as f:
    data = f.read()

offset = 0x00555C7E - PE_BASE
start = max(0, offset - 0x1000)
end = offset

chunk = data[start:end]
# Search backwards for standard prologue like `56 8B F1` or `55 8B EC` or `81 EC ...`
idx = chunk.rfind(b'\x56\x8B\xF1')
if idx != -1:
    func_start = start + idx + PE_BASE
    print(f"Found prologue 56 8B F1 at VA 0x{func_start:08X}")
else:
    idx = chunk.rfind(b'\x81\xEC')
    if idx != -1:
        func_start = start + idx + PE_BASE
        print(f"Found prologue 81 EC at VA 0x{func_start:08X}")
