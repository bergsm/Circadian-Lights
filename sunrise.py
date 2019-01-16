import controls.py 
import time 

def loadDev():
    try:
        #open device list file
        f = open("/home/pi/Circadian-Lights/device.list", "r")

    except:#TODO exception for no file
        # if no file
        controls.initDev()
        #open file
        f = open("/home/pi/Circadian-Lights/device.list", "r")

    finally:
        # load file into list
        bulbs = f.readlines()

def changeLight(bulb, targetTemp, targetBrightness):
    status = controls.getStatus()
    # if light unresponsive and last change
    if status == "error" and currTemp + tempInc == targetTemp: 
        # inf loop and wait to make change
        while(status == "error"):
            #TODO change to as fast as possible once we network directly
            time.sleep(1)
            status = controls.getStatus()
    elif status == "error" and currTemp + tempInc < targetTemp:
        return

    if status[0] == 0:
        controls.setDef(bulb, 0, temp, brightness)

    if status[0] == 1:
        controls.setlight(bulb, temp, brightness)
        controls.setDef(bulb, 0, temp, brightness)

# slowly transition the light from night to daytime
def transition():
    # get current bulb settings, specifically brightness and temp
    

    # while current bulb brightness and temp != daytime brightness and temp
        #TODO change to forking or threading for speed
        for bulb in bulbs:
            # pass device ID
            changeLight(bulb, temp, brightness)
#loadDev()
#transition()


