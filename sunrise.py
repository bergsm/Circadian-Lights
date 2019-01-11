import controls.py 


def changeLight(bulb, temp, brightness):
    status = controls.getStatus
    # if light unresponsive and last change
        # inf loop and wait to make change
    # else
        # skip this change

    # if light is responsive but off 
        controls.setDef

    # if light is responsive and on
        controls.setlight
        controls.setDef

def transition():
    # slowly transition the light from night to daytime

    # get current bulb settings, specifically brightness and temp

    # while current bulb brightness and temp != daytime brightness and temp
        changeLight(bulb, temp, brightness)


