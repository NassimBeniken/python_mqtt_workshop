import paho.mqtt.client as mqtt
from yeelight import Bulb
from pynput import keyboard
import time
import ssl

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

### Information about connection 
### ==> OK or KO with returned code
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected OK")
    else:
        print("Bad connection, returned code : " + str(rc))

### Clients subscribed to a topic will see 
### incoming messages as below and the lamps
### can be powered on or off by node red dashboard
### on the raspberry
def on_message(client, userdata, message):
    payload = str(message.payload.decode("utf-8"))
    print("message received " , payload)
    print("message topic=",message.topic)
    print("sending payload to the lamp ...")
    if message.topic == "/power1":
        if  payload == "on" or payload == "off":
            lamp_1.send_command("set_power", params= [payload])
    if message.topic == "/power2":
        if  payload == "on" or payload == "off":
            lamp_2.send_command("set_power", params= [payload])


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
client.tls_set(ca_certs = "ca.crt", cert_reqs = ssl.CERT_REQUIRED, tls_version = ssl.PROTOCOL_TLSv1_2)
client.connect(broker_address, 8883)

### Subscribing to the topics
client.subscribe("/power1")
client.subscribe("/power2")

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

### Publish a message to the corresponding topic
### when a change is detected on one of the lamps
with keyboard.Listener(on_press = on_press) as listener:
    while stop_program == False:

        if lamp_1_properties != lamp_1.get_properties(requested_properties=["power", "bright", "rgb", "name"]):
            publication = str(lamp_1.get_properties(requested_properties=["power", "bright", "rgb", "name"])).replace("\'", "\"")
            client.publish("/bulb1", publication)
            lamp_1_properties = lamp_1.get_properties(requested_properties=["power", "bright", "rgb", "name"])
            
        if lamp_2_properties != lamp_2.get_properties(requested_properties=["power", "bright", "rgb", "name"]):
            publication = str(lamp_2.get_properties(requested_properties=["power", "bright", "rgb", "name"])).replace("\'", "\"")
            client.publish("/bulb2", publication)
            lamp_2_properties = lamp_2.get_properties(requested_properties=["power", "bright", "rgb", "name"])
            
        time.sleep(3)

### Stop the loop
client.loop_stop()

### Disconnection from the  broker
client.disconnect()