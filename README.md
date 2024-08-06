# ISS tracker
This script will notify you via email when the [International Space Station (ISS)](https://www.nasa.gov/international-space-station/) is within 5 degrees of the latitude and longitude of a given location. Since the sky must be dark to view the ISS, the script will notify you only when it is night time at the given location.

The script is based on API calls for the ISS' position ([http://open-notify.org/Open-Notify-API/ISS-Location-Now/](http://open-notify.org/Open-Notify-API/ISS-Location-Now/)) and for the times of sunrise and sunset at the given location ([https://sunrise-sunset.org/api](https://sunrise-sunset.org/api)).

Inspired by the project for day 33 of the course: [100 Days of Python](https://100daysofpython.dev/).

## Installing

1. Ensure [Python](https://www.python.org/) is installed on your computer.
2. Download the Python script from this repository (that is, the `main.py` file) into the same folder.
3. Under the `# Define constants` section at the top of the script, edit the:
   - location (latitude, longitude and [time zone ID](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones))
   - email (address, password and [SMTP server name](https://sendgrid.com/en-us/blog/what-is-an-smtp-server))
5. Run `main.py`.
