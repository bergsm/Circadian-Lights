import requests

url = "https://wap.tplinkcloud.com?token=ddc8c82d-A78UG1SO4ua7acaQsH2W1rU"

header = {"Content-Type": "application/json"}

# for use if the light is off
def setDef(index):
    #hard on (with switch)
    data = '{"method":"passthrough", "params": {"deviceId": "8012CFBDD636A8E1C9B2248B3850543B19C8665F", "requestData": "{\\\"smartlife.iot.smartbulb.lightingservice\\\":{\\\"set_default_behavior\\\":{\\\"hard_on\\\":{\\\"mode\\\":\\\"customize_preset\\\",\\\"index\\\":3}}}}" }}'
    r = requests.post(url, data=data, headers=header)
    
    #soft on (with app or alexa)
    data = '{"method":"passthrough", "params": {"deviceId": "8012CFBDD636A8E1C9B2248B3850543B19C8665F", "requestData": "{\\\"smartlife.iot.smartbulb.lightingservice\\\":{\\\"set_default_behavior\\\":{\\\"soft_on\\\":{\\\"mode\\\":\\\"customize_preset\\\",\\\"index\\\":3}}}}" }}'
    r = requests.post(url, data=data, headers=header)

# for used if the light is on
#def setLight():

# used to get the current status of the light
#def getStatus():

setDef(1)
