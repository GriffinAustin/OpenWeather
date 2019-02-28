from flask import Flask, render_template
import requests
import geocoder

app = Flask(__name__)

geoloc = geocoder.ip('me')
lat = geoloc.latlng[0]
lng = geoloc.latlng[1]

api_endpoint = 'https://api.weather.gov'
api_uri = api_endpoint + '/points/{},{}'.format(str(lat), str(lng))


def get_forecast():
    r = requests.get(api_uri)
    forecast_uri = r.json()['properties']['forecast']
    r = requests.get(forecast_uri)
    today = r.json()['properties']['periods'][0]
    data = {
            'name': today['name'],
            'temperature': today['temperature'],
            'wind': today['windSpeed'] + ' ' + today['windDirection']
            }
    return data


@app.route("/")
def main():
    data = get_forecast()
    return render_template('base.html', lat=lat, lng=lng, period=data['name'], temperature=data['temperature'], wind=data['wind'])


if __name__ == "__main__":
    app.run(debug = True)
