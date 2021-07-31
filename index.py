
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pprint
import pandas as pd
import numpy as np
import plotly.express as px
import plotly
from datetime import date
import datapackage
import pandas as pd
import csv
import requests


#1. 
# Get data. https://datahub.io/cryptocurrency/bitcoin#pandas
#from datapackage import Package

#package = Package('https://datahub.io/cryptocurrency/bitcoin/datapackage.json')

# print list of all resources:
#pprint.pprint(package.resource_names)

# print processed tabular data (if exists any)
#for resource in package.resources:
   # if resource.descriptor['datahub']['type'] == 'derived/csv':
   #     pprint.pprint(resource.read())
 

#Use CoinCap API to request historical data
url = 'http://api.coincap.io/v2/assets/bitcoin/history?interval=d1'#&start=1592585794000&end=1613753794000' #can we use a variable for the unix time 1592585794000 ? 1613753794000

payload = {}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

json_data = json.loads(response.text.encode('utf8'))
bitcoin_data = json_data["data"]

#2
# create pandas dataframe
df = pd.DataFrame(bitcoin_data)
df.to_csv('bitcoin-data', index=False)
#show sample of data
print(df.sample)
#show data types
print(df.dtypes)

#create new data frame, from August 2019 to July 2021
df = pd.DataFrame(bitcoin_data, columns=['time', 'priceUSD'])
#convert priceUSD from type object to float
df['priceUSD'] = pd.to_numeric(df['priceUSD'], errors='coerce').fillna(0, downcast='infer')
#show data types
print(df.dtypes)

print(df.info)

#change unix timestamp in dataFrame to a single number i.e. 1,2,3,...9999 instead of 1564704000000, 1564790400000, 1564876800000,...1627603200000

#2019 yearly and monthly dataFrames
#df_2019 = ?
#df_August_2019 = ?

#2020 dataFrame

#2021 dataFrame


#3. 
# make separate file with the Euler game theory strategy. 

#4. 
# make graphs to visualize the price


#What we used:

#https://docs.coincap.io/
#https://www.youtube.com/watch?v=EoW4XFdh7gc