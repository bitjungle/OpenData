'''
Read weather data from frost.met.no stored in csv files.

Copyright (C) 2020 BITJUNGLE Rune Mathisen
This code is licensed under a GPLv3 license 
See http://www.gnu.org/licenses/gpl-3.0.html 
'''
import pandas as pd 
import matplotlib.pyplot as plt
import glob

path = r'data' # path to data files
datafiles = glob.glob(path + "/*.csv") # only read csv files

df_list = []
for filename in datafiles:
    df_list.append(pd.read_csv(filename)) # reading files one by one

df = pd.concat(df_list) # concatenate all dataframe objects

#print(df.head(5))

# Split the data sources
kikut = df[df['sourceId'] == 'SN30305:0']
aarhus = df[df['sourceId'] == 'SN30330:0']

# Problems with duplicates in some data files.
# https://stackoverflow.com/questions/31785371/valueerror-index-contains-duplicate-entries-cannot-reshape
kikut = kikut.drop_duplicates(['elementId','referenceTime'])
aarhus = aarhus.drop_duplicates(['elementId','referenceTime'])

# Reshape the dataframe
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.pivot.html
kikut_unfold = kikut.pivot(index='referenceTime', columns='elementId', values='value')
kikut_unfold.index = pd.DatetimeIndex(kikut_unfold.index)
aarhus_unfold = aarhus.pivot(index='referenceTime', columns='elementId', values='value')
aarhus_unfold.index = pd.DatetimeIndex(aarhus_unfold.index)

print(kikut_unfold)
print(aarhus_unfold)

#diff = kikut_unfold['air_temperature'] - aarhus_unfold['air_temperature']
#plt.plot(diff, marker='o')
#kikut_unfold['air_temperature'].plot()
#aarhus_unfold['air_temperature'].plot()
#aarhus_unfold.plot.scatter(x='air_temperature', y='wind_speed')
kikut_unfold.plot.scatter(x='air_temperature', y='wind_speed')
#kikut_unfold.plot.scatter(x='air_temperature', y='dew_point_temperature')
#kikut_unfold.plot.scatter(x='air_temperature', y='dew_point_temperature', c='wind_speed', colormap='viridis')
plt.grid()
plt.show()