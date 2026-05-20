import os

exe_path = os.path.join("..", "Bin", "SRS.exe")

with open(exe_path, "rb") as f:
    data = f.read()

# Let's search for ASCII or Unicode strings containing "camera"
print("Searching for camera-related strings...")

def search_str(s):
    ascii_bytes = s.encode("ascii")
    offset = 0
    while True:
        pos = data.find(ascii_bytes, offset)
        if pos == -1:
            break
        # Print string context
        start = max(0, pos - 10)
        end = min(len(data), pos + len(ascii_bytes) + 20)
        chunk = data[pos:pos+32]
        string_val = chunk.split(b"\x00")[0].decode("ascii", errors="ignore")
        print(f"  Found '{string_val}' at file offset 0x{pos:X} (VA 0x{pos + 0x00400000:08X})")
        offset = pos + 1

search_str("Camera")
search_str("camera")
