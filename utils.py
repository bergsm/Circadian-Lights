## Contains functions which aid the running of the program itself

import subprocess
import os
import json
import signal
import datetime

programDir = os.path.dirname(os.path.abspath(__file__))

#used for debugging
def getTime():
    return datetime.datetime.now()


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

    print(str(getTime()) + ": " + "Devices loaded successfully")
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

    print(str(getTime()) + ": " + "States loaded successfully")
    return states

def killLast():
    # check last.pid
    print(str(getTime()) + ": " + "Checking for any hanging scripts")
    try:
        f = open(programDir + "/last.pid", "r")
    except IOError:
        print(str(getTime()) + ": " + "No last.pid file found.. creating dummy file..")
        f = open(programDir + "/last.pid", "w+")
        f.write(str(-1) + "\n")
    #pid = int(f.readline())
    pids = [int(x) for x in f.read().splitlines()]
    f.close()
    os.remove(programDir + "/last.pid")

    # If script still running
    for pid in pids:
        if pid >= 0:
            #kill
            try:
                os.kill(pid, signal.SIGTERM)
            except Exception as e:
                print(str(getTime()) + ": " + "Unable to kill process " + str(pid) + ": " + str(e))
            else:
                print(str(getTime()) + ": " + "Killed " + str(pid))
        else:
            print(str(getTime()) + ": " + "Nothing to kill")


def writePID(dummy):
    if dummy == False:
        f = open(programDir + "/last.pid", "a+")
        f.write(str(os.getpid()) + "\n")
        f.close()
        print(str(getTime()) + ": " + "Wrote PID to file")
    else:
        f = open(programDir + "/last.pid", "a+")
        f.write(str(-1) + "\n")
        f.close()
        print(str(getTime()) + ": " + "Wrote dummy PID to file")
