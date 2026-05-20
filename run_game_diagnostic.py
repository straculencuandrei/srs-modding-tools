import os
import subprocess
import time

game_dir = r"c:\Program Files (x86)\Steam\steamapps\common\Street Racing Syndicate\Bin"
exe_path = os.path.join(game_dir, "SRS.EXE")
log_path = os.path.join(game_dir, "SkipIntroLog.txt")

# Clear the log file first if it exists
if os.path.exists(log_path):
    try:
        os.remove(log_path)
    except Exception as e:
        print(f"Could not remove old log: {e}")

print("Launching SRS.EXE...")
p = subprocess.Popen([exe_path], cwd=game_dir)
print(f"Launched with PID {p.pid}")

# Wait and monitor log file
start_time = time.time()
last_size = 0
while time.time() - start_time < 8.0:
    if os.path.exists(log_path):
        size = os.path.getsize(log_path)
        if size > last_size:
            with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
                f.seek(last_size)
                content = f.read()
                if content:
                    print(content, end="")
            last_size = size
    # Check if process is still running
    poll = p.poll()
    if poll is not None:
        print(f"\n[PROCESS EXIT] SRS.EXE exited with code {poll}")
        break
    time.sleep(0.1)

# Clean up
if p.poll() is None:
    print("\nTerminating SRS.EXE...")
    p.terminate()
    try:
        p.wait(timeout=2)
        print("Process terminated.")
    except subprocess.TimeoutExpired:
        print("Process did not terminate, killing...")
        p.kill()
        print("Process killed.")
