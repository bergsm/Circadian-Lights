import controls as controls
import time 
import os 
import json 


# load devices in from file
def loadDev():

    if os.path.exists("/home/pi/Circadian-Lights/devices.list"):
        f = open("/home/pi/Circadian-Lights/devices.list", "r")
        bulbs = f.read().splitlines()
    else:
        controls.initDev()
        f = open("/home/pi/Circadian-Lights/devices.list", "r")
        bulbs = f.read().splitlines()

    return bulbs


# load the relevant values in from the file
def loadStates():
    if os.path.exists("/home/pi/Circadian-Lights/values.target"):
        f = open("/home/pi/Circadian-Lights/values.target", "r")
        #text = f.readlines()
        print(text)
        states = json.loads(f.read())
    else:
        #controls.initDev()
        f = open("/home/pi/Circadian-Lights/values.target", "r")
        states = json.loads(f.read())

    return states
    
    
# change the light
def changeLight(interval, targetTemp, targetBrightness, final):
    status = controls.getStatus(bulbs[0])
    count = 0
    # if light unresponsive and last change
    if status == "error" and final == True: 
        # inf loop and wait to make change
        while(status == "error"):
            #TODO change to as fast as possible once we network directly
            time.sleep(1)
            if count < interval:
                count+=1
            status = controls.getStatus(bulbs[0])

    # if light unresponsive and not last change
    elif status == "error" and final == False:
        # wait for the specifed time interval
        while(count < interval):
            if status == "error":
                time.sleep(1)
                count+=1
            # if light comes on, change it
            elif status != "error":
                break
            # if light doesn't come on during interval, skip
            if count >= interval:
                return
    
    # if light responsive and off
    if status[0] == 0:
        # set light to be target next time turned on
        for bulb in bulbs:
            controls.setPreset(bulb, 0, targetTemp, targetBrightness)
            controls.setDef(bulb, 0)
        # wait for next command
        if count < interval:
            print("sleep time = " + str(interval-count))
            time.sleep(interval-count)
    
    # if light responsive and on
    if status[0] == 1:
        for bulb in bulbs:
            # transition light over specified length of time
            controls.setLight(bulb, interval-count, targetTemp, targetBrightness)
            # set light to be target next time turned on
            controls.setPreset(bulb, 0, targetTemp, targetBrightness)
            controls.setDef(bulb, 0)
        # wait for next command
        if count < interval:
            time.sleep(interval-count)

# slowly transition the light from night to daytime
# send 12 commands over an hour to transition light
def transition(bulbs, states):
    # get last status of lights
    status = controls.getStatus(bulbs[0]) 

    # read values for next state from file
    targetTemp = states['Evening']['Temp'] 
    targetBrightness = states['Evening']['Brightness'] 
    print("targetTemp: " + str(targetTemp))
    print("targetBrightness: " + str(targetBrightness))

    # if light off
    if status == "error" or status[0] == 0:
        # use night values for curr values
        currTemp = states['Midday(WD)']['Temp']
        currBrightness = states['Midday(WD)']['Brightness']
    # light must be on so use current values 
    else:
        currTemp = status[1]
        currBrightness = status[2]

    # interval in seconds (300 is default)
    interval = 300
    tempInt = (targetTemp - currTemp)/12
    print("tempInt " + str(tempInt))
    nextTemp = currTemp + tempInt
    
    brightInt = (targetBrightness - currBrightness)/12
    print("brightInt " + str(brightInt))
    nextBrightness = currBrightness + brightInt

    # while current bulb brightness and temp != daytime brightness and temp
    final = False
    for i in range(12):
        print(i)
        if i == 11:
            final = True
        # change the lights
        changeLight(interval, nextTemp, nextBrightness, final)

        print("currTemp = " + str(currTemp) + ", currBrightness = " + str(currBrightness))
        # set the next temps and brightnesses
        nextTemp = currTemp + tempInt
        nextBrightness = currBrightness + brightInt
        print("nextTemp = " + str(nextTemp) + ", nextBrightness = " + str(nextBrightness))
        currTemp = nextTemp
        currBrightness = nextBrightness


bulbs = loadDev()
states = loadStates()
transition(bulbs, states)
