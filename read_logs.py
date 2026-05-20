import os

log_dir = r"C:\Users\buzunar\.gemini\antigravity\brain\f9d97ec5-b10c-46a4-bdd1-84454b6ec9bf\.system_generated\logs"
overview_path = os.path.join(log_dir, "overview.txt")

if os.path.exists(overview_path):
    print("Log size:", os.path.getsize(overview_path))
    with open(overview_path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
    print("Total lines:", len(lines))
    # Print the last 150 lines
    for line in lines[-150:]:
        print(line.strip().encode('ascii', 'ignore').decode('ascii'))
else:
    print("overview.txt not found!")
