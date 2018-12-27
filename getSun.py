import requests
import json
import datetime

weather_api_token = '288eaa3e24928fe1624619297e907e5b'

geoip_api_token = 'access_key=706012c40c1b18043fdcba7c996911bd' # create account at https://darksky.net/dev/


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

location_req_url = "http://api.ipstack.com/%s?%s" % (get_ip(), geoip_api_token)
r = requests.get(location_req_url)
location_obj = json.loads(r.text)


lat = location_obj['latitude']
lon = location_obj['longitude']

#TODO add try catch logic for getting the forecast
weather_req_url = "https://api.darksky.net/forecast/%s/%s,%s?lang=%s&units=%s" % (weather_api_token, lat, lon, 'en','us')

r = requests.get(weather_req_url)
weather_obj = json.loads(r.text)

sunrise = str(weather_obj['daily']['data'][0]['sunriseTime'])
sunset = str(weather_obj['daily']['data'][0]['sunsetTime'])
f = open('/home/pi/Circadian-Lights/sun.time', 'w')

f.write(sunrise)
f.write('\n')
f.write(sunset)
f.write('\n')
f.close()

