from flask import Flask
import requests
import geocoder

app = Flask(__name__)

geoloc = geocoder.ip('me')
lat = geoloc.latlng[0]
lng = geoloc.latlng[1]

api_endpoint = 'https://api.weather.gov'
api_uri = api_endpoint + '/points/{},{}'.format(str(lat), str(lng))


@app.route("/")
def main():
    r = requests.get(api_uri)
    forecast_uri = r.json()['properties']['forecast']
    r = requests.get(forecast_uri)
    temp = r.json()['properties']['periods'][0]['temperature']
    return 'temp: ' + str(temp)


if __name__ == "__main__":
    app.run()