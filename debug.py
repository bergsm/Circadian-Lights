#import controls as controls
import controlsTest as controls

bulb1 = "8012CFBDD636A8E1C9B2248B3850543B19C8665F"
bulb2 = "8012B569B7255CD98542E8D6F1F308A319C7ACC6"
bulb3 = "80121EE053655BB04B5D29A83226E69E19C65783"


bulb1IP = "192.168.1.143"
bulb2IP = "192.168.1.102"
bulb3IP = "192.168.1.121"

url = "https://wap.tplinkcloud.com?token=ddc8c82d-A3pashRN9PvhV4s6HmfJyVe"

header = {"Content-Type": "application/json"}


#debug controls
#initDev()
#getStatus(bulb1)
#controls.setLight(bulb1, 1, 2875, 80)
#getStatus(bulb1)
#getStatus(bulb2)
#controls.setLight(bulb2, 1, 3800, 80)
controls.setLightDirect(bulb1IP, 1, 3800, 80)
controls.setLightDirect(bulb2IP, 1, 3800, 80)
controls.setLightDirect(bulb3IP, 1, 3800, 80)

#controls.setLightDirect(bulb1IP, 1, 2875, 30)
#controls.setLightDirect(bulb2IP, 1, 2875, 30)
#controls.setLightDirect(bulb3IP, 1, 2875, 30)
#controls.setPreset(bulb2, 0, 3800, 80)
#controls.setDefHard(bulb2, 0)
#controls.setDefSoft(bulb2, 0)
#getStatus(bulb2)
#getStatus(bulb3)
#controls.setLight(bulb3, 1, 3800, 80)
#getStatus(bulb3)
#getStatus(bulb1)
#setLight(bulb1, 300, 3734, 76)
#getStatus(bulb1)
