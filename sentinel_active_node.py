import time
import json
import random
import sys
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

# --- CONFIGURATION (EXTRACTED FROM YOUR OLD SCRIPT) ---
# 1. Your AWS IoT Endpoint (eu-west-1)
ENDPOINT = "a2ihz7p74rj9lu-ats.iot.eu-west-1.amazonaws.com"

# 2. Your Certificate Paths (Exact match to your old script)
PATH_TO_CERT = "./certs.crt"
PATH_TO_KEY = "./private.key"
PATH_TO_ROOT = "./AmazonRootCA1.pem"

# 3. The Topic to publish to (Required for Grafana)
TOPIC = "ev/telemetry"

# --- DYNAMIC ID LOGIC ---
# This allows the Fleet Manager to name the bus (Bus-0, Bus-1...)
if len(sys.argv) > 1:
    vehicle_id = sys.argv[1]
else:
    vehicle_id = "EV_sentinel_01"

print(f"🚀 Vehicle {vehicle_id} is starting engines...")

# --- CONNECT TO AWS ---
# We use standard MQTT Client (not Shadow) because Grafana needs a stream
myMQTTClient = AWSIoTMQTTClient(vehicle_id)
myMQTTClient.configureEndpoint(ENDPOINT, 8883)
myMQTTClient.configureCredentials(PATH_TO_ROOT, PATH_TO_KEY, PATH_TO_CERT)

print(f"📡 {vehicle_id} connecting to eu-west-1...")
try:
    myMQTTClient.connect()
    print(f"✅ {vehicle_id} CONNECTED!")
except Exception as e:
    print(f"❌ Connection Failed: {e}")
    sys.exit(1)

# --- THE SIMULATION LOOP ---
try:
    while True:
        # 1. Data simulation
        data = {
            "vehicle_id": vehicle_id,
            "timestamp": time.time(),
            "telemetry_rpm": random.randint(1000, 6000),
            "telemetry_speed": random.randint(0, 120),
            "telemetry_battery_temp": random.randint(20, 90),
            "telemetry_engine": 1,
            "coordinates": {
                "lat": -26.23 + random.uniform(-0.01, 0.01), # Soweto
                "long": 27.91 + random.uniform(-0.01, 0.01)
            }
        }
        
        # 2. Publish to AWS
        myMQTTClient.publish(TOPIC, json.dumps(data), 1)
        
        print(f"📤 {vehicle_id} published: {data['telemetry_rpm']} RPM | {data['telemetry_battery_temp']} °C")
        
        # 3. Random wait (Staggered to look real)
        time.sleep(random.uniform(1.0, 3.0))

except KeyboardInterrupt:
    print(f"\n🛑 {vehicle_id} shutting down.")
    myMQTTClient.disconnect()