import os
import struct

exe_path = os.path.join("..", "Bin", "SRS.EXE")

with open(exe_path, "rb") as f:
    data = f.read()

# Parse PE header
dos_header = data[:64]
pe_offset = struct.unpack("<I", dos_header[60:64])[0]

pe_header = data[pe_offset : pe_offset + 24]
magic, machine, num_sections = struct.unpack("<IHH", pe_header[:8])

opt_header_offset = pe_offset + 24
image_base = struct.unpack("<I", data[opt_header_offset + 28 : opt_header_offset + 32])[0]

section_headers_offset = opt_header_offset + 224 # SizeOfOptionalHeader is usually 224 for PE32

sections = []
for i in range(num_sections):
    sh_off = section_headers_offset + i * 40
    sh = data[sh_off : sh_off + 40]
    name = sh[:8].rstrip(b'\x00').decode('ascii', errors='ignore')
    vsize, vaddr, raw_size, raw_ptr = struct.unpack("<IIII", sh[8:24])
    sections.append({
        'name': name,
        'vaddr': vaddr + image_base,
        'vsize': vsize,
        'raw_ptr': raw_ptr,
        'raw_size': raw_size
    })

print(f"Image Base: 0x{image_base:08X}")
print("Sections:")
for s in sections:
    print(f"  {s['name']}: VA 0x{s['vaddr']:08X} - 0x{s['vaddr']+s['vsize']:08X} -> Raw 0x{s['raw_ptr']:X} - 0x{s['raw_ptr']+s['raw_size']:X}")

def va_to_offset(va):
    for s in sections:
        if s['vaddr'] <= va < s['vaddr'] + s['vsize']:
            return va - s['vaddr'] + s['raw_ptr']
    return None

def offset_to_va(offset):
    for s in sections:
        if s['raw_ptr'] <= offset < s['raw_ptr'] + s['raw_size']:
            return offset - s['raw_ptr'] + s['vaddr']
    return None

# Save these mappings in a global way for other scripts
print("\nTesting mapping:")
test_va = 0x00748B50
print(f"  VA 0x{test_va:08X} -> File offset 0x{va_to_offset(test_va):X}")
