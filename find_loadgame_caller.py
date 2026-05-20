import os

exe_path = os.path.join("..", "Bin", "SRS.EXE")
PE_BASE = 0x00400000

with open(exe_path, "rb") as f:
    data = f.read()

offset = 0x0040209B - PE_BASE
start = max(0, offset - 0x100)
end = min(len(data), offset + 0x10)

chunk = data[start:end]
print("Hex dump backwards from MP2PCLoadGameState constructor call:")
for i in range(0, len(chunk), 16):
    row = chunk[i:i+16]
    hex_str = " ".join(f"{b:02X}" for b in row)
    print(f"0x{start+i+PE_BASE:08X}: {hex_str}")
