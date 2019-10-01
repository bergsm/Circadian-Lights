import time
import os
import json
import socket
import utils
from struct import pack
programDir = os.path.dirname(os.path.abspath(__file__))

PORT = 9999

def encrypt(string):
    key = 171
    result = pack('>I', len(string))
    for i in string:
        a = key ^ ord(i)
        key = a
        result += chr(a)
    return result

def decrypt(string):
    key = 171
    result = ""
    for i in string:
        a = key ^ ord(i)
        key = ord(i)
        result += chr(a)
    return result

def sockSend(bulb, data):
    try:
        s =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((bulb, PORT))
        s.send(encrypt(data))
        r = s.recv(2048)
        print(decrypt(r[4:]))
        recv = decrypt(r[4:])
        s.close()
        return recv
    except socket.error:
        print(str(utils.getTime()) + ": " + "Could not connect to host " + bulb + ":" + str(PORT))
        return "error"


def changeLight(interval, currTemp, currBrightness, targetTemp, targetBrightness, final, bulb):
    start = time.time()
    status = getStatus(bulb)
    end = time.time()
    count = int(end-start)
    # if light unresponsive and last change
    if status == "error" and final == True:
        print(str(utils.getTime()) + " " + bulb + ": " + "unresponsive light and last change")
        utils.writePID(False)
        # inf loop and wait to make change
        while(status == "error"):
            print(str(utils.getTime()) + " " + bulb + ": " + "waiting...")
            start = time.time()
            status = getStatus(bulb)
            if status != "error":
                currTemp = status[1]
                currBrightness = status[2]
            end = time.time()
            if count < interval:
                count+=int(end-start)

    # if light unresponsive and not last change
    elif status == "error" and final == False:
        print(str(utils.getTime()) + " " + bulb + ": " + "unresponsive light but not last change")
        # wait for the specifed time interval
        while(count < interval):
            if status == "error":
                print(str(utils.getTime()) + " " + bulb + ": " + "waiting...")
                start = time.time()
                status = getStatus(bulb)
                if status != "error":
                    currTemp = status[1]
                    currBrightness = status[2]
                end = time.time()
                count+=int(end-start)
            # if light comes on, change it
            elif status != "error":
                print(str(utils.getTime()) + " " + bulb + ": " + "light now on!")
                break
            # if light doesn't come on during interval, skip
            if count >= interval:
                print(str(utils.getTime()) + " " + bulb + ": " + "skipping..")
                return


    # if light responsive and off
    if status[0] == 0:
        print(str(utils.getTime()) + " " + bulb + ": " + "light responsive and off")
        # set light to be target next time turned on
        start = time.time()
        setPreset(bulb, 0, targetTemp, targetBrightness)
        setDef(bulb, 0)
        end = time.time()
        count += int(end-start)
        # wait for next command
        if count < interval:
            print(str(utils.getTime()) + " " + bulb + ": " + "sleep time = " + str(interval-count))
            time.sleep(interval-count)


    # if light responsive and on
    if status[0] == 1:
        print(str(utils.getTime()) + " " + bulb + ": " + "light responsive and on")

        # I split this into two loops to have the actual changing of each light closer together
        start = time.time()
        # Manual override detection. Only change light if no manual override detected
        if status[1] == currTemp and status[2] == currBrightness:
            # transition light over specified length of time
            transition = max(interval-count, 1)
            print(str(utils.getTime()) + " " + bulb + ": " + "Transition period: " + str(transition))
            setLight(bulb, transition, targetTemp, targetBrightness)
        else:
            print(str(utils.getTime()) + " " + bulb + ": " + "Manual override detected, only changing default behavior")

        # set light to be target next time turned on
        setPreset(bulb, 0, targetTemp, targetBrightness)
        setDef(bulb, 0)

        end = time.time()
        count += int(end-start)

        # wait for next command
        if count < interval:
            print(str(utils.getTime()) + " " + bulb + ": " + "sleep time = " + str(interval-count))
            time.sleep(interval-count)



def changeLights(interval, currTemp, currBrightness, targetTemp, targetBrightness, final, bulb):
    start = time.time()
    status = getStatus(bulb)
    end = time.time()
    count = int(end-start)
    # if light unresponsive and last change
    if status == "error" and final == True:
        print(str(utils.getTime()) + " " + bulb + ": " + "unresponsive light and last change")
        utils.writePID(False)
        # inf loop and wait to make change
        while(status == "error"):
            print(str(utils.getTime()) + " " + bulb + ": " + "waiting...")
            start = time.time()
            status = getStatus(bulb)
            if status != "error":
                currTemp = status[1]
                currBrightness = status[2]
            end = time.time()
            if count < interval:
                count+=int(end-start)

    # if light unresponsive and not last change
    elif status == "error" and final == False:
        print(str(utils.getTime()) + " " + bulb + ": " + "unresponsive light but not last change")
        # wait for the specifed time interval
        while(count < interval):
            if status == "error":
                print(str(utils.getTime()) + " " + bulb + ": " + "waiting...")
                start = time.time()
                status = getStatus(bulb)
                if status != "error":
                    currTemp = status[1]
                    currBrightness = status[2]
                end = time.time()
                count+=int(end-start)
            # if light comes on, change it
            elif status != "error":
                print(str(utils.getTime()) + " " + bulb + ": " + "light now on!")
                break
            # if light doesn't come on during interval, skip
            if count >= interval:
                print(str(utils.getTime()) + " " + bulb + ": " + "skipping..")
                return


    # if light responsive and off
    if status[0] == 0:
        print(str(utils.getTime()) + " " + bulb + ": " + "light responsive and off")
        # set light to be target next time turned on
        start = time.time()
        setPreset(bulb, 0, targetTemp, targetBrightness)
        setDef(bulb, 0)
        end = time.time()
        count += int(end-start)
        # wait for next command
        if count < interval:
            print(str(utils.getTime()) + " " + bulb + ": " + "sleep time = " + str(interval-count))
            time.sleep(interval-count)


    # if light responsive and on
    if status[0] == 1:
        print(str(utils.getTime()) + " " + bulb + ": " + "light responsive and on")

        # I split this into two loops to have the actual changing of each light closer together
        start = time.time()
        # Manual override detection. Only change light if no manual override detected
        if status[1] == currTemp and status[2] == currBrightness:
            # transition light over specified length of time
            transition = max(interval-count, 1)
            print(str(utils.getTime()) + " " + bulb + ": " + "Transition period: " + str(transition))
            setLight(bulb, transition, targetTemp, targetBrightness)
        else:
            print(str(utils.getTime()) + " " + bulb + ": " + "Manual override detected, only changing default behavior")

        # set light to be target next time turned on
        setPreset(bulb, 0, targetTemp, targetBrightness)
        setDef(bulb, 0)

        end = time.time()
        count += int(end-start)

        # wait for next command
        if count < interval:
            print(str(utils.getTime()) + " " + bulb + ": " + "sleep time = " + str(interval-count))
            time.sleep(interval-count)


#TODO consolidate set default functions and change light functions?

def setDef(bulb, index):
    setDefHard(bulb, index)
    setDefSoft(bulb, index)

# change the default behavior of the light bulb when turned on by switch to a preset index
def setDefHard(bulb, index):
    data = '{"smartlife.iot.smartbulb.lightingservice":{"set_default_behavior":{"hard_on":{"mode":"customize_preset","index":' + str(index) + '}}}}'
    sockSend(bulb, data)

# change the default behavior of the light bulb when turned on by software to a preset index
def setDefSoft(bulb, index):
    data = '{"smartlife.iot.smartbulb.lightingservice":{"set_default_behavior":{"soft_on":{"mode":"customize_preset","index":' + str(index) + '}}}}'
    sockSend(bulb, data)

# change the light
# transition time should be in seconds
def setLight(bulb, trans, temp, brightness):
    trans = trans * 1000
    data = '{"smartlife.iot.smartbulb.lightingservice":{"transition_light_state":{"ignore_default":1, "transition_period":'+ str(trans) + ', "on_off":1, "color_temp":' + str(temp) + ', "brightness":' + str(brightness) + '}}}'
    sockSend(bulb, data)

# change a preset
def setPreset(bulb, index, temp, brightness):
    data = '{"smartlife.iot.smartbulb.lightingservice":{"set_preferred_state":{"saturation":0,"index":' + str(index) + ',"hue":0,"color_temp":' + str(temp) + ',"brightness":' + str(brightness) + '}}}'
    sockSend(bulb, data)

# used to get the current status of the light
def getStatus(bulb):
    data = '{"smartlife.iot.smartbulb.lightingservice":{"get_light_state":""}}'
    r = sockSend(bulb, data)
    if r == "error":
        return r
    else:
        response = json.loads(r)
    if response['smartlife.iot.smartbulb.lightingservice']['get_light_state']['err_code'] == 0:
        on_off = response['smartlife.iot.smartbulb.lightingservice']['get_light_state']['on_off']
        if on_off == 0:
            temp = 0
            brightness = 0
        else:
            temp = response['smartlife.iot.smartbulb.lightingservice']['get_light_state']['color_temp']
            brightness = response['smartlife.iot.smartbulb.lightingservice']['get_light_state']['brightness']
        #print(on_off, temp, brightness)
        return[on_off, temp, brightness]
    else:
        return "error"
