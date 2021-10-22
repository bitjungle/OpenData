'''
Download weather data from frost.met.no.
Based on https://frost.met.no/python_example.html

Copyright (C) 2020 BITJUNGLE Rune Mathisen
This code is licensed under a GPLv3 license 
See http://www.gnu.org/licenses/gpl-3.0.html 
'''
import requests
import pandas as pd
import datetime
from os.path import exists

# Specify year span for data retrieval
year_start = 2014
year_stop = 2021

# Enter your own client ID
# https://frost.met.no/auth/requestCredentials.html
client_id = 'YOUR_CLIENT_ID_HERE'

# Specify data sources
# See NO-sources.json
data_sources = 'SN30305, SN30330'

# Specify data elements
# https://frost.met.no/concepts2.html#element
# Find elements for a specific data source (needs client id):
# https://frost.met.no/api.html#!/observations/timeSeries
data_elements = 'air_temperature, dew_point_temperature, wind_speed'

# Specify output folder
output_folder = 'data'

# Todays date
now = datetime.datetime.now()

# Collecting data for one month at a time
for year in range(year_start, year_stop + 1):
    for month in range(1, 13):

        if year == now.year and month == now.month:
            # Cannot collect data from the future :-) 
            break

        # Constructing referencetime
        if month == 12:
            year_end = year + 1
            month_end = 1
        else:
            year_end = year 
            month_end = month + 1
        ref_time = '{0}-{2:02}-01/{1}-{3:02}-01'.format(year, year_end, month, month_end)
        print('Requesting data from {} for time period {}'.format(data_sources, ref_time))

        # Output csv file name
        file_name = '{}/{}-{:02}.csv'.format(output_folder, year, month)
        if exists(file_name):
            # We already have data for this month
            print(file_name, 'exists already')
        else:
            print('Writing data to {}'.format(file_name))

            # Define endpoint and parameters
            # Time specification: https://frost.met.no/concepts2.html#timespecifications
            endpoint = 'https://frost.met.no/observations/v0.jsonld'
            parameters = {
                'sources': data_sources,
                'elements': data_elements,
                'referencetime': ref_time,
            }
            # Issue an HTTP GET request
            print('Requesting data from frost.met.no...')
            r = requests.get(endpoint, parameters, auth=(client_id,''))
            # Extract JSON data
            json = r.json()

            # Check if the request worked, print out any errors
            if r.status_code == 200:
                data = json['data']
                print('...data retrieved from frost.met.no')
            else:
                print('Error! Returned status code %s' % r.status_code)
                print('Message: %s' % json['error']['message'])
                print('Reason: %s' % json['error']['reason'])
                break

            # This will return a Dataframe with all of the observations in a table format
            print('Constructing dataframe...')
            df = pd.DataFrame()
            for i in range(len(data)):
                row = pd.DataFrame(data[i]['observations'])
                row['referenceTime'] = data[i]['referenceTime'].replace('.000Z', '').replace('T', ' ')
                row['sourceId'] = data[i]['sourceId']
                df = df.append(row)
            df = df.reset_index()
            print('...done')

            print('Writing to file...')
            df.to_csv(file_name)
            print('...done')
