import os
import subprocess
import time
import ctypes
from ctypes import wintypes

PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_VM_READ = 0x0010
MAX_PATH = 260

psapi = ctypes.WinDLL('psapi', use_last_error=True)
kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

psapi.EnumProcessModules.argtypes = [
    wintypes.HANDLE,
    ctypes.POINTER(wintypes.HMODULE),
    wintypes.DWORD,
    ctypes.POINTER(wintypes.DWORD)
]
psapi.EnumProcessModules.restype = wintypes.BOOL

psapi.GetModuleFileNameExW.argtypes = [
    wintypes.HANDLE,
    wintypes.HMODULE,
    wintypes.LPWSTR,
    wintypes.DWORD
]
psapi.GetModuleFileNameExW.restype = wintypes.DWORD

game_dir = r"c:\Program Files (x86)\Steam\steamapps\common\Street Racing Syndicate\Bin"
exe_path = os.path.join(game_dir, "SRS.exe")

print("Launching SRS.exe in the foreground...")
# Start process normally
p = subprocess.Popen([exe_path], cwd=game_dir)
print(f"Launched PID {p.pid}. Sleeping 8 seconds for game window and modules to initialize...")
time.sleep(8.0)

h_process = kernel32.OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, False, p.pid)
if not h_process:
    print(f"Failed to open process: {ctypes.get_last_error()}")
    p.terminate()
    exit(0)

try:
    h_modules = (wintypes.HMODULE * 1024)()
    cb_needed = wintypes.DWORD()
    if psapi.EnumProcessModules(h_process, h_modules, ctypes.sizeof(h_modules), ctypes.byref(cb_needed)):
        num_modules = cb_needed.value // ctypes.sizeof(wintypes.HMODULE)
        print(f"\nLoaded modules ({num_modules}):")
        found_asi = []
        for i in range(num_modules):
            h_mod = h_modules[i]
            buf = ctypes.create_unicode_buffer(MAX_PATH)
            if psapi.GetModuleFileNameExW(h_process, h_mod, buf, MAX_PATH):
                mod_path = buf.value
                if ".asi" in mod_path.lower() or "skipintro" in mod_path.lower() or "varioushacks" in mod_path.lower():
                    found_asi.append(mod_path)
                print(f"  {mod_path}")
        print("\n=== ASI Loading Verification ===")
        if found_asi:
            print("Found loaded ASI modules:")
            for asi in found_asi:
                print(f"  [+] {asi}")
        else:
            print("[WARNING] No ASI modules are loaded! The ASI loader is NOT working!")
    else:
        print(f"EnumProcessModules failed: {ctypes.get_last_error()}")
finally:
    kernel32.CloseHandle(h_process)
    print("\nTerminating SRS.exe...")
    p.terminate()
    p.wait()
