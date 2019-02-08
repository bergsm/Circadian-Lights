import controls as controls
import time 
import os 
import json 
import signal


programDir = os.path.dirname(os.path.abspath(__file__))

# load devices in from file
def loadDev():

    if os.path.exists(programDir + "/devices.list"):
        f = open(programDir + "/devices.list", "r")
        bulbs = f.read().splitlines()
        f.close()
    else:
        controls.initDev()
        f = open(programDir + "/devices.list", "r")
        bulbs = f.read().splitlines()
        f.close()

    print("Devices loaded successfully")
    return bulbs


# load the relevant values in from the file
def loadStates():
    if os.path.exists(programDir + "/values.target"):
        f = open(programDir + "/values.target", "r")
        states = json.loads(f.read())
        f.close()
    else:
        states = {"Night":{"Temp":2700,"Brightness":1},\
                  "Evening":{"Temp":2875,"Brightness":30},\
                  "Midday":{"Temp":3800,"Brightness":80}}
        f = open(programDir + "/values.target", "w+")
        f.write(json.dumps(states))
        f.close()

    print("States loaded successfully")
    return states


def killLast():
    # check last.pid
    print("Checking for any hanging scripts")
    f = open(programDir + "/last.pid", "r")
    pid = int(f.readline())
    f.close()
    
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
        f = open(programDir + "/last.pid", "w+")
        f.write(str(os.getpid()))
        f.close()
        print("Wrote PID to file")
    else:
        f = open(programDir + "/last.pid", "w+")
        f.write(str(-1))
        f.close()
        print("Wrote dummy PID to file")


# change the light
def changeLight(interval, currTemp, currBrightness, targetTemp, targetBrightness, final):
    start = time.time()
    status = controls.getStatus(bulbs[0])
    end = time.time()
    count = int(end-start)
    # if light unresponsive and last change
    if status == "error" and final == True: 
        print("unresponsive light and last change")
        writePID(True)
        # inf loop and wait to make change
        while(status == "error"):
            print("waiting...")
            start = time.time()
            status = controls.getStatus(bulbs[0])
            if status != "error":
                currTemp = status[1]
                currBrightness = status[2]
            end = time.time()
            if count < interval:
                count+=int(end-start)

    # if light unresponsive and not last change
    elif status == "error" and final == False:
        print("unresponsive light but not last change")
        # wait for the specifed time interval
        while(count < interval):
            if status == "error":
                print("waiting...")
                start = time.time()
                status = controls.getStatus(bulbs[0])
                if status != "error":
                    currTemp = status[1]
                    currBrightness = status[2]
                end = time.time()
                count+=int(end-start)
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
        start = time.time()
        for bulb in bulbs:
            controls.setPreset(bulb, 0, targetTemp, targetBrightness)
            controls.setDef(bulb, 0)
        end = time.time()
        count += int(end-start)
        # wait for next command
        if count < interval:
            print("sleep time = " + str(interval-count))
            time.sleep(interval-count)


    # if light responsive and on
    if status[0] == 1:
        print("light responsive and on")

        # I split this into two loops to have the actual changing of each light closer together
        start = time.time()
        # Manual override detection. Only change light if no manual override detected
        if status[1] == currTemp and status[2] == currBrightness:
            for bulb in bulbs:
                # transition light over specified length of time
                transition = max(interval-count, 1)
                print("Transition period: " + str(transition))
                controls.setLight(bulb, transition, targetTemp, targetBrightness)
        else:
            print("Manual override detected, only changing default behavior")

        for bulb in bulbs:
            # set light to be target next time turned on
            controls.setPreset(bulb, 0, targetTemp, targetBrightness)
            controls.setDef(bulb, 0)

        end = time.time()
        count += int(end-start)

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
    targetTemp = states['Night']['Temp'] 
    targetBrightness = states['Night']['Brightness'] 
    print("targetTemp: " + str(targetTemp))
    print("targetBrightness: " + str(targetBrightness))

    # if light off
    if status == "error" or status[0] == 0:
        # use last state values for curr values
        currTemp = states['Evening']['Temp']
        currBrightness = states['Evening']['Brightness']
    # light must be on so use current values 
    else:
        currTemp = status[1]
        currBrightness = status[2]

    # interval in seconds
    interval = 150
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
        changeLight(interval, currTemp, currBrightness, nextTemp, nextBrightness, final)

        currTemp = nextTemp
        currBrightness = nextBrightness

killLast()
bulbs = loadDev()
states = loadStates()
transition(bulbs, states)
writePID(False)
