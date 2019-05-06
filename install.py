#!/bin/python

import controls
import os
import sys

if os.getuid() != 0:
    print('Error: install.py needs to be run as root.\nUse \"sudo install.py\"\n')
    sys.exit(1)

#TODO check and download requirements if not installed

# Congratulate user on downloading Circadian-Lights
welcome = "Hello! Welcome to Sun Lights! You're about to install Sun Lights into your new home!"\
          "\n Setup should only take a few minutes\n. You just need to answer a couple of questions"\
          " to customize your lighting solution, and we'll take care of the rest!"
print(welcome)

print("First we're going to scan your network for TP-Link Devices that are compatible with Sun Lights. Is that ok?\n")

ans = raw_input("[yes/no]")
if 'y' in ans:
    print("Ok! This shouldn't take long...")
    #TODO add feedback for what devices were found
    controls.initDev()
    print("Done! Your devices have been saved. You can manually add or edit your devices later by editing the devices.list file\n")

else:
    print("Ok. You can manually add devices at a later time by creating or editing the devices.list file\n")

#TODO install getSun script into cron scheduling

#TODO prompt user for timing of transition relative to sunrise and sunset. (This would involve modifying getSun)

#TODO run getSun script once to set up sunRise and sunSet times.

#TODO sense the time of day and transition bulbs to correct brightness

print("Congratulations! Your system is all set up and ready to go!)

