import controls as controls


bulb1 = "192.168.1.143"
bulb2 = "192.168.1.102"
bulb3 = "192.168.1.121"

url = "https://wap.tplinkcloud.com?token=ddc8c82d-A3pashRN9PvhV4s6HmfJyVe"

header = {"Content-Type": "application/json"}


#debug controls
#initDev()
controls.getStatus(bulb3)
#controls.setLight(bulb1, 1, 2875, 80)
#getStatus(bulb1)
#getStatus(bulb2)
controls.setLight(bulb3, 1, 2700, 1)
controls.getStatus(bulb3)
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
