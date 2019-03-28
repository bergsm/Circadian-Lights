#!/usr/bin/python
#import night as trans

interval = 1

def test(targetTemp, currTemp, targetBrightness, currBrightness):
    print(targetTemp - currTemp)
    tempInt = int(round((targetTemp - currTemp)/12.0))
    print(tempInt)
    print("tempInt " + str(tempInt))

    brightInt = int(round((targetBrightness - currBrightness)/12.0))
    print(brightInt)
    print("brightInt " + str(brightInt))

    # while current bulb brightness and temp != daytime brightness and temp
    final = False
    for i in range(12):
        print(i)
        print("currTemp = " + str(currTemp) + ", currBrightness = " + str(currBrightness))
        nextTemp = currTemp + tempInt
        nextBrightness = currBrightness + brightInt
        if i == 11:
            final = True
            nextTemp = targetTemp
            nextBrightness = targetBrightness
        # change the lights
        print("nextTemp = " + str(nextTemp) + ", nextBrightness = " + str(nextBrightness))
        changeLight(interval, nextTemp, nextBrightness, final)

        # set the next temps and brightnesses
        currTemp = nextTemp
        currBrightness = nextBrightness


test(2875, 3800, 30, 85)
