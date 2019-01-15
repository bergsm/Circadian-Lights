import requests
import json
import socket

bulb1 = "8012CFBDD636A8E1C9B2248B3850543B19C8665F"

url = "https://wap.tplinkcloud.com?token=ddc8c82d-A78UG1SO4ua7acaQsH2W1rU"

header = {"Content-Type": "application/json"}

def debug(request):
    print(request.text)

# change the default behavior of the light bulb when turned on by switch to a preset index
def setDefHard(bulb, index):
    #hard on (with switch)
    data = '{"method":"passthrough", "params": {"deviceId": "' + bulb + '", "requestData": "{\\\"smartlife.iot.smartbulb.lightingservice\\\":{\\\"set_default_behavior\\\":{\\\"hard_on\\\":{\\\"mode\\\":\\\"customize_preset\\\",\\\"index\\\":' + str(index) + '}}}}" }}'
    r = requests.post(url, data=data, headers=header)
    #debug(r)
    
# change the default behavior of the light bulb when turned on by software to a preset index
def setDefSoft(bulb, index):
    #soft on (with app or alexa)
    data = '{"method":"passthrough", "params": {"deviceId": "' + bulb + '", "requestData": "{\\\"smartlife.iot.smartbulb.lightingservice\\\":{\\\"set_default_behavior\\\":{\\\"soft_on\\\":{\\\"mode\\\":\\\"customize_preset\\\",\\\"index\\\":' + str(index) + '}}}}" }}'
    r = requests.post(url, data=data, headers=header)
    #debug(r)

# change the light
def setLight(bulb, temp, brightness):
    data = '{"method":"passthrough", "params": {"deviceId": "' + bulb + '", "requestData": "{\\\"smartlife.iot.smartbulb.lightingservice\\\":{\\\"transition_light_state\\\":{\\\"ignore_default\\\":1, \\\"on_off\\\":1, \\\"color_temp\\\":' + str(temp) + ', \\\"brightness\\\":' + str(brightness) + '}}}" }}'
    r = requests.post(url, data=data, headers=header)
    #debug(r)

# change a preset
def setPreset(bulb, index, temp, brightness):
    data = '{"method":"passthrough", "params": {"deviceId": "' + bulb + '", "requestData": "{\\\"smartlife.iot.smartbulb.lightingservice\\\":{\\\"set_preferred_state\\\":{\\\"saturation\\\":0,\\\"index\\\":' + str(index) + ',\\\"hue\\\":0,\\\"color_temp\\\":' + str(temp) + ',\\\"brightness\\\":' + str(brightness) + '}}}" }}'
    r = requests.post(url, data=data, headers=header)
    #debug(r)

# used to get the current status of the light
def getStatus(bulb):
    data = '{"method":"passthrough", "params": {"deviceId": "' + bulb + '", "requestData": "{\\\"smartlife.iot.smartbulb.lightingservice\\\":{\\\"get_light_state\\\":\\\"\\\"}}" }}'     
    r = requests.post(url, data=data, headers=header)
    debug(r)

# initialize the file for the dictionary of the devices and their IDs
def initDev():
    data = '{method:getDeviceList}'
    r = requests.post(url, data=data, headers=header)
    response = json.loads(r.text)
    #TODO substitute user env variable for pi
    f = open('/home/pi/Circadian-Lights/devices.list', 'w+')
    for each in response['result']['deviceList']:
        f.write(each['deviceId'] + "\n")
    #debug(r)

#initDev()
getStatus(bulb1)
#setLight(bulb1, 3545, 75)
#setDefHard(bulb1, 1)
#setDefSoft(bulb1, 1)
#setPreset(bulb1, 0, 3800, 80)
