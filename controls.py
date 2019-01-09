import requests

bulb1 = "8012CFBDD636A8E1C9B2248B3850543B19C8665F"

url = "https://wap.tplinkcloud.com?token=ddc8c82d-A78UG1SO4ua7acaQsH2W1rU"

header = {"Content-Type": "application/json"}

def debug(request):
    print(request.text)

# change the default behavior of the light bulb when turned on by switch to a preset index
def setDefHard(index):
    #hard on (with switch)
    data = '{"method":"passthrough", "params": {"deviceId": "8012CFBDD636A8E1C9B2248B3850543B19C8665F", "requestData": "{\\\"smartlife.iot.smartbulb.lightingservice\\\":{\\\"set_default_behavior\\\":{\\\"hard_on\\\":{\\\"mode\\\":\\\"customize_preset\\\",\\\"index\\\":1}}}}" }}'
    r = requests.post(url, data=data, headers=header)
    debug(r)
    
# change the default behavior of the light bulb when turned on by software to a preset index
def setDefSoft(index):
    #soft on (with app or alexa)
    data = '{"method":"passthrough", "params": {"deviceId": "8012CFBDD636A8E1C9B2248B3850543B19C8665F", "requestData": "{\\\"smartlife.iot.smartbulb.lightingservice\\\":{\\\"set_default_behavior\\\":{\\\"soft_on\\\":{\\\"mode\\\":\\\"customize_preset\\\",\\\"index\\\":1}}}}" }}'
    r = requests.post(url, data=data, headers=header)
    debug(r)

# change the light
#def setLight():

# change a preset
def setPreset(index, temp, brightness):
    data = '{"method":"passthrough", "params": {"deviceId": "' + bulb1 + '", "requestData": "{\\\"smartlife.iot.smartbulb.lightingservice\\\":{\\\"set_preferred_state\\\":{\\\"saturation\\\":0,\\\"index\\\":1,\\\"hue\\\":0,\\\"color_temp\\\":3800,\\\"brightness\\\":80}}}" }}'
    r = requests.post(url, data=data, headers=header)
    debug(r)

# used to get the current status of the light
#def getStatus():

setDefHard(1)
setDefSoft(1)
setPreset(0, 3800, 80)
