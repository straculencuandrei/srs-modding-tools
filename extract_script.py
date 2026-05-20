import mmap
import os

archive_path = os.path.join("..", "Data", "archive.ar")

with open(archive_path, "rb") as f:
    mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
    
    # The main game data script starts at the START section before InitialCash
    # InitialCash is at 0x2CF378BA, START is a bit before that
    # Let's find START near that location
    
    search_start = 0x2CF37800
    idx = mm.find(b"START", search_start)
    print(f"START found at: 0x{idx:08X}")
    
    # Find END after it 
    end_idx = mm.find(b"\r\nEND\r\n", idx)
    print(f"END found at: 0x{end_idx:08X}")
    
    script_data = mm[idx:end_idx + 5]  # include END
    print(f"Script size: {len(script_data)} bytes")
    
    # Decode and save the full game data script
    text = script_data.decode('ascii', errors='replace')
    
    with open("MP2GAMEDATA_SCRIPT.txt", "w") as out:
        out.write(text)
    
    print(f"\nSaved to MP2GAMEDATA_SCRIPT.txt")
    print(f"\nFirst 2000 chars:")
    print(text[:2000])
    print(f"\n...\n\nLast 500 chars:")
    print(text[-500:])
    
    mm.close()
