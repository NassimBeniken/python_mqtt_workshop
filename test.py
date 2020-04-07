from yeelight import Bulb
import time
from deepdiff import DeepDiff
from pynput import keyboard

### Create a bulb with IP of the light
#lamp_1 = Bulb("192.168.1.16")
#lamp_2 = Bulb("192.168.1.17")

### Get the properties of the light
#properties = lamp_1.get_properties()

### Turn the light on or off
#lamp_1.turn_on()
#lamp_2.turn_on()
#lamp_1.turn_off()
#lamp_2.turn_off()

### Send a command to the light
#lamp_1.send_command("set_power", params= ["on"])
#lamp_1.send_command("start_cf", params = [0, 0, "1000, 2, 2700, 100, 500, 1, 255, 10, 50, 7, 0,0, 500, 2, 5000, 1"])


############# TESTS #############
lamp_1 = Bulb("192.168.1.16")
lamp_2 = Bulb("192.168.1.17")

lamp_1.set_name("Lamp 1")
lamp_2.set_name("Lamp 2")

lamp_1_properties = lamp_1.get_properties()
lamp_2_properties = lamp_2.get_properties()

print("Properties lamp 1 : " + str(lamp_1_properties))
print("\n")
print("Properties lamp 2 : " + str(lamp_2_properties))

stop_program = False

def on_press(key):
    global stop_program
    print (key)
    if key == keyboard.Key.cmd:
        print ('end pressed')
        stop_program = True
        return False

with keyboard.Listener(on_press = on_press) as listener:
    while stop_program == False:
        if lamp_1_properties != lamp_1.get_properties() or lamp_2_properties != lamp_2.get_properties():
            if lamp_1_properties != lamp_1.get_properties():
                publication = "Lamp 1 : " + str(DeepDiff(lamp_1_properties, lamp_1.get_properties()))
                print(publication)
                print("\n")
                lamp_1_properties = lamp_1.get_properties()
            
            if lamp_2_properties != lamp_2.get_properties():
                publication = "Lamp 2 : " + str(DeepDiff(lamp_2_properties, lamp_2.get_properties()))
                print(publication)
                print("\n")
                lamp_2_properties = lamp_2.get_properties()
        else:
            print("No changes \n")
        time.sleep(10)

