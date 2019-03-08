import subprocess
import os
import json
import socket
from struct import pack

#TODO port 1040 might be the UDP port
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
        print("Could not connect to host " + bulb + ":" + str(PORT))
        return "error"

#def debug(request):
#    print(request.text)

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

# initialize the file for the dictionary of the devices and their IDs
def initDev():
    programDir = os.path.dirname(os.path.abspath(__file__))
    # call bash script to save network devices to file
    subprocess.call(programDir + "/bash/devIP.sh")

    # open network list for reading
    fin = open(programDir + '/network.list', 'r')
    fout = open(programDir + '/devices.list', 'w+')
    text = fin.readlines()
    for line in text:
        # TODO look for other TP-Link devices that will work with this code
        if line[0:5] == "LB130":
            for i in range(0, len(line)):
                if line[i] == '(':
                    IP = line[i+1:i+14]
                    fout.write(IP + "\n")

    # delete network.list file
    os.remove(programDir + '/network.list')
