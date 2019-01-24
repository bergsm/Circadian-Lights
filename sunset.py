import controls as controls
import time 
import os 
import json 
import signal


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
    #TODO remove conditional or flesh out else statement
    if os.path.exists("/home/pi/Circadian-Lights/values.target"):
        f = open("/home/pi/Circadian-Lights/values.target", "r")
        #text = f.readlines()
        #print(text)
        states = json.loads(f.read())
    else:
        #controls.initDev()
        f = open("/home/pi/Circadian-Lights/values.target", "r")
        states = json.loads(f.read())

    return states


def killLast():
    # check last.pid
    print("Checking for any hanging scripts")
    f = open("/home/pi/Circadian-Lights/last.pid", "r")
    pid = int(f.readline())
    
    # If script still running
    if pid >= 0:
        #kill
        try:
            os.kill(pid, signal.SIGTERM)
        except:
            print("Unable to kill previous process")
        else:
            print("Killed " + str(pid))
    else:
        print("Nothing to kill")


def writePID(hanging):
    if hanging == True:
        f = open("/home/pi/Circadian-Lights/last.pid", "w+")
        f.write(str(os.getpid()))
        print("Wrote PID to file")
    else:
        f = open("/home/pi/Circadian-Lights/last.pid", "w+")
        f.write(str(-1))
        print("Wrote dummy PID to file")
 

# change the light
def changeLight(interval, targetTemp, targetBrightness, final):
    status = controls.getStatus(bulbs[0])
    count = 0
    # if light unresponsive and last change
    if status == "error" and final == True: 
        print("unresponsive light and last change")
        writePID(True)
        # inf loop and wait to make change
        while(status == "error"):
            #TODO change to as fast as possible once we network directly
            time.sleep(1)
            print("waiting...")
            if count < interval:
                count+=1
            status = controls.getStatus(bulbs[0])

    # if light unresponsive and not last change
    elif status == "error" and final == False:
        print("unresponsive light but not last change")
        # wait for the specifed time interval
        while(count < interval):
            if status == "error":
                print("waiting...")
                time.sleep(1)
                count+=1
                status = controls.getStatus(bulbs[0])
            # if light comes on, change it
            elif status != "error":
                print("light now on!")
                break
            # if light doesn't come on during interval, skip
            if count >= interval:
                print("skipping..")
                return
    
    # if light responsive and off
    if status[0] == 0:
        print("light responsive and off")
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
        print("light responsive and on")
        for bulb in bulbs:
            # transition light over specified length of time
            controls.setLight(bulb, interval-count, targetTemp, targetBrightness)
        for bulb in bulbs:
            # set light to be target next time turned on
            controls.setPreset(bulb, 0, targetTemp, targetBrightness)
            controls.setDef(bulb, 0)
        # wait for next command
        if count < interval:
            print("sleep time = " + str(interval-count))
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
    tempInt = int((targetTemp - currTemp)/12.0)
    print("tempInt " + str(tempInt))
    
    brightInt = int((targetBrightness - currBrightness)/12.0)
    print("brightInt " + str(brightInt))

    # while current bulb brightness and temp != daytime brightness and temp
    final = False
    for i in range(12):
        print(i)
        print("currTemp = " + str(currTemp) + ", currBrightness = " + str(currBrightness))
        
        # set the next temps and brightnesses
        nextTemp = currTemp + tempInt
        nextBrightness = currBrightness + brightInt
        
        if i == 11:
            final = True
            nextTemp = targetTemp
            nextBrightness = targetBrightness
        
        # change the lights
        print("nextTemp = " + str(nextTemp) + ", nextBrightness = " + str(nextBrightness))
        changeLight(interval, nextTemp, nextBrightness, final)

        currTemp = nextTemp
        currBrightness = nextBrightness

killLast()
bulbs = loadDev()
states = loadStates()
transition(bulbs, states)
writePID(False)
