import controls as controls
import os
import json
import signal
import utils
import sys

if (len(sys.argv) < 2):
    print("Error: No transition state argument")
    exit(1)

programDir = os.path.dirname(os.path.abspath(__file__))

def killLast():
    # check last.pid
    print("Checking for any hanging scripts")
    try:
        f = open(programDir + "/last.pid", "r")
    except IOError:
        print("No last.pid file found.. creating dummy file..")
        f = open(programDir + "/last.pid", "w+")
        f.write(str(-1))
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

# slowly transition the light from night to daytime
# send 12 commands over an hour to transition light
#def transition(bulbs, states):
def transition():
    # load devices and states into memory
    bulbs = utils.loadDev()
    states = utils.loadStates()

    # set current and next states
    nextState = sys.argv[1]
    currState = states[nextState]['Prev']
    print("Curr State: " + currState)
    print("Next State: "  + nextState)

    # get last status of lights
    status = controls.getStatus(bulbs[0])

    # read values for next state from file
    targetTemp = states[nextState]['Temp']
    targetBrightness = states[nextState]['Brightness']
    print("targetTemp: " + str(targetTemp))
    print("targetBrightness: " + str(targetBrightness))

    # if light off
    if status == "error" or status[0] == 0:
        # use last state values for curr values
        currTemp = states[currState]['Temp']
        currBrightness = states[currState]['Brightness']
    # light must be on so use current values
    else:
        currTemp = status[1]
        currBrightness = status[2]

    # interval in seconds
    #TODO uncomment when finished testing
    #interval = 150
    interval = sys.argv[2]
    print("Interval: " + str(interval))
    tempInt = int(round((targetTemp - currTemp)/12.0))
    print("tempInt " + str(tempInt))

    brightInt = int(round((targetBrightness - currBrightness)/12.0))
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
        controls.changeLights(interval, currTemp, currBrightness, nextTemp, nextBrightness, final, bulbs)

        currTemp = nextTemp
        currBrightness = nextBrightness

killLast()
transition()
writePID(False)
