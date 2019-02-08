import controls as controls
from random import randint

bulb1 = "192.168.1.143"
bulb2 = "192.168.1.102"
bulb3 = "192.168.1.121"

bulbs = [bulb1, bulb2, bulb3]

#while(1):
#    controls.setLightOff(bulbs[randint(0,2)], 0, 3800, 100)
#    controls.setLight(bulbs[randint(0,2)], 0, 3800, 100)
#debug controls

controls.lightShow(bulbs, 40)

#for i in range(0, 5):
#    for bulb in bulbs:
#        controls.setLightOff(bulb, 0, 3800, 100)
#    for bulb in bulbs:
#        controls.setLight(bulb, 0, 3800, 100)
#
#for i in range(0, 5):
#    for bulb in reversed(bulbs):
#        controls.setLightOff(bulb, 0, 3800, 100)
#    for bulb in reversed(bulbs):
#        controls.setLight(bulb, 0, 3800, 100)

#for i in range(0, 10):
#    for bulb in bulbs:
#        controls.setLightOff(bulb, 0, 3800, 100)
#    for bulb in bulbs:
#        controls.setLight(bulb, 0, 3800, 100)


#controls.setLightOff(bulb1, 0, 3800, 100)
#controls.setLightOff(bulb2, 0, 3800, 100)
#controls.setLightOff(bulb3, 0, 3800, 100)
#controls.setLight(bulb1, 0, 3800, 100)
#controls.setLight(bulb2, 0, 3800, 100)
#controls.setLight(bulb3, 0, 3800, 100)



#controls.setLightOff(bulb1, 0, 3800, 100)
#initDev()
#controls.setLight(bulb1, 0, 3800, 100)
#controls.setLightOff(bulb1, 0, 3800, 100)
#getStatus(bulb1)
#getStatus(bulb2)
#controls.setLight(bulb3, 1, 2700, 1)
#controls.getStatus(bulb3)
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
