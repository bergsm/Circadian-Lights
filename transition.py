import controls
import utils
import sys


# slowly transition the light from night to daytime
# send 12 commands over an hour to transition light

# Time in minutes for entire transition
if (len(sys.argv) == 3):
    transPeriod = int(sys.argv[2])
else:
    transPeriod = 60

if (len(sys.argv) < 2):
    print(str(utils.getTime()) + ": " + "Error: No transition state argument")
    exit(1)

# Time in seconds for each interval in transition
interval = transPeriod/12 * 60

# if transitioning to night, take half the time
if (sys.argv[1] == 'Night'):
    interval = interval/2

#check for any unfinished transitions and write PID to file
utils.killLast()
utils.writePID(False)

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
print("Interval: " + str(interval))
tempInt = int(round((targetTemp - currTemp)/12.0))
print("tempInt " + str(tempInt))

brightInt = int(round((targetBrightness - currBrightness)/12.0))
print("brightInt " + str(brightInt))

# while current bulb brightness and temp != daytime brightness and temp
final = False
for i in range(12):
    print(str(utils.getTime()) + ": " + str(i))
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

#write dummy PID to file
utils.writePID(True)
