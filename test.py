from yeelight import Bulb

### Create a bulb with IP of the light
bulb = Bulb("192.168.1.16")

### Get the properties of the light
#properties = bulb.get_properties()

### Turn the light on or off
#bulb.turn_on()
#bulb.turn_off()

### Send a command to the light
bulb.send_command("set_power", params= ["off"])
#bulb.send_command("start_cf", params = [0, 0, "1000, 2, 2700, 100, 500, 1, 255, 10, 50, 7, 0,0, 500, 2, 5000, 1"])
