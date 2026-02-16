import subprocess
import time

NUM_VEHICLES = 10 
processes = []

for i in range(NUM_VEHICLES):
    vehicle_id = f"Bus-{i:02d}"
    p = subprocess.Popen(["python", "sentinel_active_node.py", vehicle_id])
    processes.append(p)
    print(f"🚀 Launched {vehicle_id}")
    time.sleep(5)

try:
    while True: time.sleep(5)
except KeyboardInterrupt:
    for p in processes: p.terminate()
    print("Fleet Grounded.")