import os
import shutil

def patch_initial_cash(archive_path, new_cash):
    print(f"Modifying InitialCash to {new_cash}...")
    
    # Check if backup exists, if not create one
    backup_path = archive_path + ".bak"
    if not os.path.exists(backup_path):
        print("Creating backup of archive.ar...")
        shutil.copy2(archive_path, backup_path)
    
    with open(archive_path, 'r+b') as f:
        data = f.read()
        
        # Find InitialCash block
        search_str = b"InitialCash\r\n"
        idx = data.find(search_str)
        if idx == -1:
            print("Error: Could not find InitialCash in archive.")
            return
            
        value_start = idx + len(search_str)
        value_end = data.find(b"\r\n", value_start)
        
        current_val_str = data[value_start:value_end]
        print(f"Current cash value: {current_val_str.decode('ascii')}")
        
        new_val_str = str(new_cash).encode('ascii')
        
        len_diff = len(new_val_str) - len(current_val_str)
        
        if len_diff > 0:
            # We need to shrink the file elsewhere to maintain exact file size
            # We will remove '\r' characters from nearby newlines to compensate
            print(f"Need to remove {len_diff} padding bytes...")
            
            # Find '\r' characters after the value
            search_idx = value_end
            bytes_removed = 0
            
            # We will construct the new data chunk
            # Replace the cash value
            before = data[:value_start]
            after = data[value_end:]
            
            new_data = bytearray(before + new_val_str + after)
            
            # Now remove len_diff '\r' characters
            search_idx = value_start + len(new_val_str)
            
            while bytes_removed < len_diff:
                r_idx = new_data.find(b"\r\n", search_idx)
                if r_idx == -1:
                    print("Error: Could not find enough newlines to trim!")
                    return
                
                # Remove the '\r'
                del new_data[r_idx]
                bytes_removed += 1
                search_idx = r_idx + 1 # move past the '\n'
            
            # Ensure total size matches
            assert len(new_data) == len(data), "Size mismatch after modification!"
            
            f.seek(0)
            f.write(new_data)
            print("Successfully updated archive with new cash value!")
            
        elif len_diff < 0:
            # We need to pad the value
            # Since it's a number, we can pad with leading zeros (e.g. 0000)
            padded_val = f"{new_cash:0{len(current_val_str)}d}".encode('ascii')
            f.seek(value_start)
            f.write(padded_val)
            print("Successfully updated archive with new cash value (padded)!")
        else:
            # Same length, direct overwrite
            f.seek(value_start)
            f.write(new_val_str)
            print("Successfully updated archive with new cash value!")

if __name__ == "__main__":
    archive_file = os.path.join("..", "Data", "archive.ar")
    if os.path.exists(archive_file):
        try:
            # Change this to whatever amount you want
            desired_cash = 9999999
            patch_initial_cash(archive_file, desired_cash)
        except Exception as e:
            print(f"Error: {e}")
    else:
        print(f"Could not find {archive_file}")
