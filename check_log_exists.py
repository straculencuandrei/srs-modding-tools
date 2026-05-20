import os

game_dir = r"c:\Program Files (x86)\Steam\steamapps\common\Street Racing Syndicate\Bin"
root_dir = r"c:\Program Files (x86)\Steam\steamapps\common\Street Racing Syndicate"

log1 = os.path.join(game_dir, "SkipIntroLog.txt")
log2 = os.path.join(root_dir, "SkipIntroLog.txt")

if os.path.exists(log1):
    print(f"Log found in Bin! Size: {os.path.getsize(log1)} bytes")
    with open(log1, "r") as f:
        print(f.read())
elif os.path.exists(log2):
    print(f"Log found in Root! Size: {os.path.getsize(log2)} bytes")
    with open(log2, "r") as f:
        print(f.read())
else:
    print("No SkipIntroLog.txt found anywhere in Bin or Root!")
