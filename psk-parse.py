import paho.mqtt.client as mqtt
import json

# Define the desired sender and receiver country codes
desired_sender_country = 327
desired_receiver_country = 291

# Define the desired partial grid
desired_partial_grid = "CN86"

# Callback when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # Subscribe to all topics under pskr/filter/v2/
    client.subscribe("pskr/filter/v2/#")

# Callback when a message is received from the broker
def on_message(client, userdata, msg):
    payload = msg.payload.decode('utf-8')
    data = json.loads(payload)

    # Check if the sender and receiver countries match the desired values
    sender_country = data.get('sa')
    receiver_country = data.get('ra')
    
    # Check if the sender or receiver locator contains the desired partial grid
    sender_locator = data.get('sl', "")[:4]  # Take the first 4 characters
    receiver_locator = data.get('rl', "")[:4]  # Take the first 4 characters    

    if (
        (sender_country == desired_sender_country and receiver_country == desired_receiver_country) or
        (sender_country == desired_receiver_country and receiver_country == desired_sender_country)
    ) and (
        desired_partial_grid in sender_locator or
        desired_partial_grid in receiver_locator
    ):
       
        # Print information about the matching spot
        print(f"Received matching spot:")
        print(f"  Sender: {data['sc']}")
        print(f"  Receiver: {data['rc']}")
        print(f"  Band: {data['b']}")
        print(f"  Mode: {data['md']}")
        print(f"  SNR: {data['rp']}")
        print(f"  Sender Locator: {data['sl']}")
        print(f"  Receiver Locator: {data['rl']}")
        print(f"  Sender Country: {sender_country}")
        print(f"  Receiver Country: {receiver_country}")
        print(f"  Frequency: {data['f']}")
        print(f"  Time: {data['t']}")
        print("-------------------")

# Create an MQTT client instance
client = mqtt.Client()

# Set the callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker
client.connect("mqtt.pskreporter.info", 1883, 60)

# Run the client loop in a blocking manner
client.loop_forever()
