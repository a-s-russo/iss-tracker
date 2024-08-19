import os
import smtplib
import time
from datetime import datetime

import requests

# Define constants
MY_EMAIL = os.environ.get("MY_EMAIL")
MY_PASSWORD = os.environ.get("MY_PASSWORD")
MY_LAT = float(os.environ.get("MY_LAT"))
MY_LNG = float(os.environ.get("MY_LNG"))
MY_TZ = os.environ.get("MY_TZ")
MY_SMTP = os.environ.get("MY_SMTP")

# Create cache to store sunrise and sunset times for each day
cache = {}


def is_iss_overhead():
    response = requests.get(url='http://api.open-notify.org/iss-now.json')
    response.raise_for_status()
    data = response.json()
    iss_latitude = float(data['iss_position']['latitude'])
    iss_longitude = float(data['iss_position']['longitude'])
    return MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LNG - 5 <= iss_longitude <= MY_LNG + 5


def is_night():
    global cache

    # Current time and date
    now = datetime.now().astimezone()
    date_today = now.strftime('%Y-%m-%d')

    # Retrieve sunrise and sunset times from cache if available, otherwise fetch via API call
    if date_today in cache:
        sunrise = cache[date_today]['sunrise']
        sunset = cache[date_today]['sunset']
    else:
        parameters = {
            'lat': MY_LAT,
            'lng': MY_LNG,
            'formatted': 0,
            'tzid': MY_TZ,
        }

        # Get sunrise and sunset times
        response = requests.get(url='https://api.sunrise-sunset.org/json', params=parameters)
        response.raise_for_status()
        data = response.json()

        # Sunrise
        sunrise_string = data['results']['sunrise']
        sunrise_date_string = sunrise_string.split('T')[0]
        sunrise_time_string = sunrise_string.split('T')[1].split('+')[0]
        sunrise_datetime_string = sunrise_date_string + ' ' + sunrise_time_string
        sunrise = datetime.strptime(sunrise_datetime_string, '%Y-%m-%d %H:%M:%S').astimezone()

        # Sunset
        sunset_string = data['results']['sunset']
        sunset_date_string = sunset_string.split('T')[0]
        sunset_time_string = sunset_string.split('T')[1].split('+')[0]
        sunset_datetime_string = sunset_date_string + ' ' + sunset_time_string
        sunset = datetime.strptime(sunset_datetime_string, '%Y-%m-%d %H:%M:%S').astimezone()

        # Cache times
        times = {'sunrise': sunrise, 'sunset': sunset}
        cache[date_today] = times

    return now <= sunrise or now >= sunset


while True:
    if is_night() and is_iss_overhead():
        timestamp = datetime.now().astimezone().strftime('%Y-%m-%d %H:%M')
        with smtplib.SMTP(MY_SMTP) as connection:
            connection.starttls()
            connection.login(MY_EMAIL, MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=MY_EMAIL,
                msg=f'Subject:Look up! \n\nThe ISS is above you in the sky!\n\nTimestamp: {timestamp}'
            )
        break
    time.sleep(300)
