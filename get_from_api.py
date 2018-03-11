'''
Requests data from the weather api.

Http gzip compression should be enabled.
'''

import requests
import instance.config # modify this once flask is set up *****

dark_sky_call = (
        'https://api.darksky.net/forecast/'
        + instance.config.DARK_SKY_API_KEY + '/'
        + str(instance.config.LATITUDE) + ','
        + str(instance.config.LONGITUDE))
call_options = {'units': 'si', 'extend': 'hourly'}
call_headers = {'Accept-Encoding': 'gzip'}

r = requests.get(dark_sky_call, params=call_options, headers=call_headers)

print(r.url)
print(r.text)
