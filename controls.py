import requests

url = "https://wap.tplinkcloud.com?token=ddc8c82d-A78UG1SO4ua7acaQsH2W1rU"

header = {'Content-Type': 'application/json'}

# for use if the light is off
def setDef(index):
    r = requests.post(url, data={"method":"passthrough","params":{"deviceId":"8012CFBDD636A8E1C9B2248B3850543B19C8665F","requestData":{"smartlife.iot.smartbulb.lightingservice":{"set_default_behavior":{"soft_on":{"mode":"customize_preset","index":3,"hue":0,"saturation":0,"color_temp":2500,"brightness":30}}}}}, headers=header)
    print(r.status_code)
    print(r.text)

# for used if the light is on
#def setLight():

# used to get the current status of the light
#def getStatus():

setDef(1)
