import requests
import json
import datetime
from subprocess import Popen, PIPE, call

# Useful tokens
weather_api_token = '288eaa3e24928fe1624619297e907e5b'
geoip_api_token = 'access_key=706012c40c1b18043fdcba7c996911bd' # create account at https://darksky.net/dev/

#update filesystem data base and locate sunrise and sunset scripts
def findScripts():
    scriptLoc = []
    call(['sudo', 'updatedb'])
    sunrise = Popen(['locate', 'transition.py'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = sunrise.communicate(b"input data that is passed to subprocess' stdin")
    filepaths = output.splitlines()

    scriptLoc.append(filepaths[0])

    return scriptLoc

# get the ip address for use later in geo location
def get_ip():
    try:
        ip_url = "http://jsonip.com/"
        req = requests.get(ip_url)
        ip_json = json.loads(req.text)
        return ip_json['ip']
    except Exception as e:
        f.write("Error: %s." %e)
        traceback.print_exc()
        return "Error: %s. Cannot get ip." % e

# Get the location from the ip address
location_req_url = "http://api.ipstack.com/%s?%s" % (get_ip(), geoip_api_token)
r = requests.get(location_req_url)
location_obj = json.loads(r.text)
# get the latitude and longitude
lat = location_obj['latitude']
lon = location_obj['longitude']

# get the local forecast for sunrise and sunset time
#TODO add try catch logic for getting the forecast
weather_req_url = "https://api.darksky.net/forecast/%s/%s,%s?lang=%s&units=%s" % (weather_api_token, lat, lon, 'en','us')
r = requests.get(weather_req_url)
weather_obj = json.loads(r.text)


#update filesystem data base and locate sunrise and sunset scripts
scriptLoc = findScripts()

# Parse out the sunrise and sunset time and convert to cron format
sunriseEpoch = str(weather_obj['daily']['data'][0]['sunriseTime'])
sunrise = (datetime.datetime.fromtimestamp(float(sunriseEpoch))-datetime.timedelta(hours=0, minutes=45)).strftime('%M %H')
srCronCmd = sunrise + " * * * pi /usr/bin/python " + scriptLoc[0] + " Midday >> /home/pi/Circadian-Lights/cron.log 2>&1\n"
#print(srCronCmd)

sunsetEpoch = str(weather_obj['daily']['data'][0]['sunsetTime'])
sunset = (datetime.datetime.fromtimestamp(float(sunsetEpoch))-datetime.timedelta(hours=0, minutes=45)).strftime('%M %H')
ssCronCmd = sunset + " * * * pi /usr/bin/python " + scriptLoc[0] + " Evening >> /home/pi/Circadian-Lights/cron.log 2>&1\n"
#print(ssCronCmd)

# Schedule crontab jobs to run at sunrise and sunset
f2 = open('/etc/cron.d/sunriseCron', 'w')
f3 = open('/etc/cron.d/sunsetCron', 'w')
f2.write(srCronCmd)
f3.write(ssCronCmd)
f2.close()
f3.close()
