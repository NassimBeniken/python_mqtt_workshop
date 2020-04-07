import paho.mqtt.client as mqtt
from yeelight import Bulb
from deepdiff import DeepDiff
from pynput import keyboard
import time

### Setting the lamps
lamp_1 = Bulb("192.168.1.16")
lamp_2 = Bulb("192.168.1.17")

lamp_1.set_name("Lamp 1")
lamp_2.set_name("Lamp 2")

lamp_1_properties = lamp_1.get_properties(requested_properties=["power", "bright", "rgb", "name"])
lamp_2_properties = lamp_2.get_properties(requested_properties=["power", "bright", "rgb", "name"])

### Logging function
def on_log(client, userdata, level, buf):
    print("log : " + buf)

### Information about connection ==> OK or KO with returned code
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conected OK")
    else:
        print("Bad connection, returned code : " + str(rc))

### Clients subscribed to a topic will see incoming messages as below
def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)

### Boker address
broker_address = "nakebenihime.ddns.net"

### Client instance creation
client = mqtt.Client("Beni")
client.username_pw_set("pi","raspberry")

client.on_connect = on_connect
client.on_log = on_log
client.on_message = on_message

### Connection to the broker
print("Connecting to the broker")
client.connect(broker_address, 18830)

### Start the loop to process the callback
client.loop_start()

### Keyboard listener function
stop_program = False

def on_press(key):
    global stop_program
    print (key)
    if key == keyboard.Key.cmd:
        print ('end pressed')
        stop_program = True
        return False

### Publish a message to a topic when a change is detected
with keyboard.Listener(on_press = on_press) as listener:
    while stop_program == False:
        if lamp_1_properties != lamp_1.get_properties(requested_properties=["power", "bright", "rgb", "name"]):
            publication = str(lamp_1.get_properties(requested_properties=["power", "bright", "rgb", "name"])).replace("\'", "\"")
            client.publish("/helloworld", publication)
            lamp_1_properties = lamp_1.get_properties(requested_properties=["power", "bright", "rgb", "name"])
            
        if lamp_2_properties != lamp_2.get_properties(requested_properties=["power", "bright", "rgb", "name"]):
            publication = str(lamp_2.get_properties(requested_properties=["power", "bright", "rgb", "name"])).replace("\'", "\"")
            client.publish("/helloworld2", publication)
            lamp_2_properties = lamp_2.get_properties(requested_properties=["power", "bright", "rgb", "name"])
        time.sleep(3)

### Stop the loop
client.loop_stop()

### Disconnection from the  broker
client.disconnect()