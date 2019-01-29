import requests
import json
import socket
from struct import pack

bulb1 = "8012CFBDD636A8E1C9B2248B3850543B19C8665F"
bulb2 = "8012B569B7255CD98542E8D6F1F308A319C7ACC6"
bulb3 = "80121EE053655BB04B5D29A83226E69E19C65783"

bulb1IP = "192.168.1.143"
bulb2IP = "192.168.1.102"
bulb3IP = "192.168.1.121"

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

url = "https://wap.tplinkcloud.com?token=ddc8c82d-A3pashRN9PvhV4s6HmfJyVe"

header = {"Content-Type": "application/json"}

def debug(request):
    print(request.text)

def setDef(bulb, index):
    setDefHard(bulb, index)
    setDefSoft(bulb, index)

# change the default behavior of the light bulb when turned on by switch to a preset index
def setDefHard(bulb, index):
    #hard on (with switch)
    data = '{"method":"passthrough", "params": {"deviceId": "' + bulb + '", "requestData": "{\\\"smartlife.iot.smartbulb.lightingservice\\\":{\\\"set_default_behavior\\\":{\\\"hard_on\\\":{\\\"mode\\\":\\\"customize_preset\\\",\\\"index\\\":' + str(index) + '}}}}" }}'
    r = requests.post(url, data=data, headers=header)
    debug(r)
    
# change the default behavior of the light bulb when turned on by software to a preset index
def setDefSoft(bulb, index):
    #soft on (with app or alexa)
    data = '{"method":"passthrough", "params": {"deviceId": "' + bulb + '", "requestData": "{\\\"smartlife.iot.smartbulb.lightingservice\\\":{\\\"set_default_behavior\\\":{\\\"soft_on\\\":{\\\"mode\\\":\\\"customize_preset\\\",\\\"index\\\":' + str(index) + '}}}}" }}'
    r = requests.post(url, data=data, headers=header)
    debug(r)

# change the light
# transition time should be in seconds
def setLight(bulb, trans, temp, brightness):
    trans = trans * 1000
    data = '{"method":"passthrough", "params": {"deviceId": "' + bulb + '", "requestData": "{\\\"smartlife.iot.smartbulb.lightingservice\\\":{\\\"transition_light_state\\\":{\\\"ignore_default\\\":1, \\\"transition_period\\\":'+ str(trans) + ', \\\"on_off\\\":1, \\\"color_temp\\\":' + str(temp) + ', \\\"brightness\\\":' + str(brightness) + '}}}" }}'
    r = requests.post(url, data=data, headers=header)
    debug(r)

def setLightDirect(bulb, trans, temp, brightness):
    #TODO change to direct message with bulb via socket
    trans = trans * 1000
    data = '{"smartlife.iot.smartbulb.lightingservice":{"transition_light_state":{"ignore_default":1, "transition_period":' + str(trans) + ', "on_off":1, "color_temp":' + str(temp) + ', "brightness":' + str(brightness) + '}}}'


    try:
        s =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((bulb, PORT))
        s.send(encrypt(data))
        r = s.recv(2048)
        print(decrypt(r[4:]))
        s.close()
    except socket.error:
        print("Could not connect to host " + bulb1IP + ":" + str(port))
        
    
    #r = requests.post(url, data=data, headers=header)


# change a preset
def setPreset(bulb, index, temp, brightness):
    data = '{"method":"passthrough", "params": {"deviceId": "' + bulb + '", "requestData": "{\\\"smartlife.iot.smartbulb.lightingservice\\\":{\\\"set_preferred_state\\\":{\\\"saturation\\\":0,\\\"index\\\":' + str(index) + ',\\\"hue\\\":0,\\\"color_temp\\\":' + str(temp) + ',\\\"brightness\\\":' + str(brightness) + '}}}" }}'
    r = requests.post(url, data=data, headers=header)
    debug(r)

# used to get the current status of the light
def getStatus(bulb):
    data = '{"method":"passthrough", "params": {"deviceId": "' + bulb + '", "requestData": "{\\\"smartlife.iot.smartbulb.lightingservice\\\":{\\\"get_light_state\\\":\\\"\\\"}}" }}'     
    r = requests.post(url, data=data, headers=header)
    debug(r)
    response = json.loads(r.text)
    if response['error_code'] == 0:
        bulbStatus = json.loads((response['result']['responseData']))
        on_off = bulbStatus['smartlife.iot.smartbulb.lightingservice']['get_light_state']['on_off']
        if on_off == 0:
            temp = 0
            brightness = 0
        else:
            temp = bulbStatus['smartlife.iot.smartbulb.lightingservice']['get_light_state']['color_temp']
            brightness = bulbStatus['smartlife.iot.smartbulb.lightingservice']['get_light_state']['brightness']
        #print(on_off, temp, brightness)
        return[on_off, temp, brightness]
    else:
        return "error"

# initialize the file for the dictionary of the devices and their IDs
def initDev():
    data = '{method:getDeviceList}'
    r = requests.post(url, data=data, headers=header)
    response = json.loads(r.text)
    #TODO substitute user env variable for pi
    f = open('/home/pi/Circadian-Lights/devices.list', 'w+')
    for each in response['result']['deviceList']:
        f.write(each['deviceId'] + "\n")
    debug(r)

