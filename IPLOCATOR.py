# write a python function that takes an IP address as an argument and returns the location (char(2)) of the IP address.

import requests
import json
import os
import sys
import time




from pydantic import IPvAnyNetwork, IPvAnyAddress
API_KEY = os.environ.get('APIKEY_IPSTACK')
def get_IP_location(IP: IPvAnyAddress):
    # API key for ipstack.com


    try:
        url = f'http://api.ipstack.com/{IP}?access_key={API_KEY}&format=1'
    except:
        return None

    try :
        response = requests.get(url)
        CC = response.json()['country_code']
        print(f'Country Code: {CC}')
        return CC

    except Exception as e:
        print(f"Error: {e}")
        return None








