import paho.mqtt.client as mqtt

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
broker_address = "83.114.113.20"

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

### Publish a message to a topic
client.publish("/helloworld", "Tu me casses les couilles")

### Stop the loop
client.loop_stop()

### Disconnection from the  broker
client.disconnect()