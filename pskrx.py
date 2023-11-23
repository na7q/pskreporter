import paho.mqtt.client as mqtt
import json

# Callback when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # Subscribe to the topic of interest
    #client.subscribe("pskr/filter/v2/#")
    client.subscribe("pskr/filter/v2/+/+/+/+/+/+/+/327")

# Callback when a message is received from the broker
def on_message(client, userdata, msg):
    payload = msg.payload.decode('utf-8')
    data = json.loads(payload)
    print(f"Received spot:")
    print(f"  Sender: {data['sc']}")
    print(f"  Receiver: {data['rc']}")
    print(f"  Band: {data['b']}")
    print(f"  Mode: {data['md']}")
    print(f"  SNR: {data['rp']}")
    print(f"  Sender Locator: {data['sl']}")
    print(f"  Receiver Locator: {data['rl']}")
    print(f"  Sender Country: {data['sa']}")
    print(f"  Receiver Country: {data['ra']}")
    print(f"  Frequency: {data['f']}")
    print(f"  Time: {data['t']}")

# Create an MQTT client instance
client = mqtt.Client()

# Set the callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker
client.connect("mqtt.pskreporter.info", 1883, 60)

# Run the client loop in a blocking manner
client.loop_forever()
