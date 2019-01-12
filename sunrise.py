import controls.py 

def loadDev():
    # if no file
        controls.initDev()
    # load file into dictionary

def changeLight(bulb, temp, brightness):
    status = controls.getStatus()
    # if light unresponsive and last change
        # inf loop and wait to make change
    # else
        # skip this change

    # if light is responsive but off 
        controls.setDef(bulb, 0, temp, brightness)

    # if light is responsive and on
        controls.setlight(bulb, temp, brightness)
        controls.setDef(bulb, 0, temp, brightness)

def transition():
    # slowly transition the light from night to daytime

    # get current bulb settings, specifically brightness and temp

    # while current bulb brightness and temp != daytime brightness and temp
        #TODO change to forking or threading for speed
        for bulb in bulbs:
            # pass device ID
            changeLight(bulb, temp, brightness)
#loadDev()
#transition()


