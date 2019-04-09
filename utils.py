import subprocess
import os
import json

programDir = os.path.dirname(os.path.abspath(__file__))

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
        if line[0:5].upper() == "LB130":
            for i in range(0, len(line)):
                if line[i] == '(':
                    IP = line[i+1:i+14]
                    fout.write(IP + "\n")

    # delete network.list file
    os.remove(programDir + '/network.list')

# load devices from storage into memory
def loadDev():
    if os.path.exists(programDir + "/devices.list"):
        f = open(programDir + "/devices.list", "r")
        bulbs = f.read().splitlines()
        f.close()
    else:
        initDev()
        f = open(programDir + "/devices.list", "r")
        bulbs = f.read().splitlines()
        f.close()

    print("Devices loaded successfully")
    return bulbs

#Load the user specified light states from storage into memory
def loadStates():
    if os.path.exists(programDir + "/values.target"):
        f = open(programDir + "/values.target", "r")
        states = json.loads(f.read())
        f.close()
    else:
        states = {"Night":{"Temp":2700,"Brightness":1},\
                  "Evening":{"Temp":2875,"Brightness":30},\
                  "Midday":{"Temp":3630,"Brightness":85}}
        f = open(programDir + "/values.target", "w+")
        f.write(json.dumps(states))
        f.close()

    print("States loaded successfully")
    return states
