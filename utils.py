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
        states = {"Night":{"Temp":2700,"Brightness":1, "Prev":"Evening"},\
                "Evening":{"Temp":2875,"Brightness":35, "Prev":"Midday"},\
                "Midday":{"Temp":3635,"Brightness":85, "Prev":"Night"}}
        f = open(programDir + "/values.target", "w+")
        f.write(json.dumps(states))
        f.close()

    print("States loaded successfully")
    return states

def killLast():
    # check last.pid
    print("Checking for any hanging scripts")
    try:
        f = open(programDir + "/last.pid", "r")
    except IOError:
        print("No last.pid file found.. creating dummy file..")
        f = open(programDir + "/last.pid", "w+")
        f.write(str(-1))
    pid = int(f.readline())
    f.close()

    # If script still running
    if pid >= 0:
        #kill
        try:
            os.kill(pid, signal.SIGTERM)
        except:
            print("Unable to kill previous process")
        else:
            print("Killed " + str(pid))
    else:
        print("Nothing to kill")
