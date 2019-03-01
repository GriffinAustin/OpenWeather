from flask import Flask, render_template
import requests
import geocoder

app = Flask(__name__)

# Get geolocation of user
geoloc = geocoder.ip('me')
lat = geoloc.latlng[0]
lng = geoloc.latlng[1]

# Define API
api_endpoint = 'https://api.weather.gov'
api_uri = api_endpoint + '/points/{},{}'.format(str(lat), str(lng))
r = requests.get(api_uri)
loc = r.json()['properties']['relativeLocation']['properties']['city'] + ', ' + r.json()['properties']['relativeLocation']['properties']['state']

def get_forecast():
    # Retrieve uri
    r = requests.get(api_uri)
    forecast_uri = r.json()['properties']['forecast']
    r = requests.get(forecast_uri)

    # Loop through forecast data
    properties = r.json()['properties']
    periods = r.json()['properties']['periods']
    num_of_periods = len(periods)
    data = {}
    for i in range(num_of_periods):
        sub_data = {
                    'name': periods[i]['name'],
                    'temperature': periods[i]['temperature']
                    }
        data.update({str(i): sub_data})
    return data


@app.route("/")
def main():
    data = get_forecast()
    return render_template('base.html', loc=loc, lat=lat, lng=lng, data=data)


if __name__ == "__main__":
    app.run(debug = True)
