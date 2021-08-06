from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pprint
import pandas as pd
import numpy as np
import plotly.express as px
import plotly
from datetime import date, datetime
import datapackage
import csv
import requests
import matplotlib.pyplot as plt
import math

#Supressing SettingWithCopyWarning
pd.options.mode.chained_assignment = None  # default='warn'

#==============================================================================================================================
#Tasks:
#A
#change unix timestamp in dataFrame to a number based on date i.e. 08012019 instead of 1564704000000

#create new data frames
#2019 yearly and monthly dataFrames
#df_2019 = ?
#df_August_2019 = ?

#2020 dataFrame

#2021 dataFrame

#B
#Tensorflow idea

#C
#jupyter notebook in google colab

#D
#use matplotlib to make a graph in step 4
 
#==============================================================================================================================

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
 

def convertFromUnixTimeToDateTime(unixTime):
   return datetime.utcfromtimestamp(unixTime/1000).strftime('%m%d%Y')

def assignMonth(numMonth):
   month = {
      "01":"January",
      "02":"February",
      "03":"March",
      "04":"April",
      "05":"May",
      "06":"June",
      "07":"July",
      "08":"August",
      "09":"September",
      "10":"October",
      "11":"Novemeber",
      "12":"December"
   }

   return month.get(str(numMonth)[0:2], "Error")

def eulerStoppingTheory(data):
   # Determing number of days to set as sample data
   numberOfDays = len(data.index)
   sampleSize = math.ceil(numberOfDays/math.e)

   # Splitting data into sample and test data. 
   # Sample Dataframe Range: [0, sampleSize]
   # Test Dataframe Range: [sampleSize + 1, numberOfDays]
   sampleDf = data.iloc[:sampleSize,:]
   testDf = data.iloc[sampleSize:,:]

   # Storing minimum and maximum value of sample range
   maxSampleValue = sampleDf['priceUsd'].max()
   minSampleValue = sampleDf['priceUsd'].min()

   # Storing minimum and maximum value of test range
   maxPossibleTestValue = testDf['priceUsd'].max()
   minPossibleTestValue = testDf['priceUsd'].min()

   # Initializing variable to store the first possible value that is greater than or equal to (or less than or equal to) to the max and min of the sample data
   maxSelectedTestValue = None
   minSelectedTestValue = None

   # Looking for the first value in test data that is larger than the largest data point in sample dataset
   for max in testDf['priceUsd']:
      if max >= maxSampleValue:
         maxSelectedTestValue = max
         break

   # Looking for the first value in test data that is larger than the largest data point in sample dataset
   for min in testDf['priceUsd']:
      if min <= minSampleValue:
         minSelectedTestValue = min
         break
   
   # Storing collected results in array
   listOfValues = [minSampleValue, maxSampleValue, minPossibleTestValue, maxPossibleTestValue, minSelectedTestValue, maxSelectedTestValue]

   # Returning array
   return listOfValues

########################### ONLY USED ONCE TO STORE SPECIFC DATA LOCALLY ################################################################################
#Use CoinCap API to request historical data
#url = 'http://api.coincap.io/v2/assets/bitcoin/history?interval=d1'#&start=1592585794000&end=1613753794000' #can we use a variable for the unix time 1592585794000 ? 1613753794000

#payload = {}
#headers = {}

#response = requests.request("GET", url, headers=headers, data=payload)

#json_data = json.loads(response.text.encode('utf8'))
#bitcoin_data = json_data["data"]

#2
# create pandas dataframe
#df = pd.DataFrame(bitcoin_data)
#df.to_csv('bitcoin-data', index=False)
########################### ONLY USED ONCE TO STORE SPECIFC DATA LOCALLY ################################################################################

#Creating dataframe that stores data [priceUSD, time, date] from website to pandas dataframe
df = pd.read_csv('bitcoin-data')

#Convert time values from Unix Time to datatime [Month Day Year]
df['time'] = df['time'].apply(convertFromUnixTimeToDateTime)

#Adding new column that stores what month the piece of data is from
df['month'] = df['time'].apply(assignMonth)

monthlyData = None
months = {"August", "September", "October", "November", "December", "January", "February", "March", "April", "May", "June", "July"}

#3. 
# make separate file with the Euler game theory strategy. 

#Initializing container to store results of applying optimal stopping theory
# Key is the MonthYear
# Value is an array that contains a list of values (list of values listed in eulerStoppingTheory method)
dict = {}

for year in range(2019, 2022):
   for month in months:
      # Storing subset of data based on month and year
      monthlyData = df[df['month'].str.contains(month) & df['date'].str.contains(str(year))]

      #Checks to make sure that there is data to be processed
      if not monthlyData.empty:
         # Applys optimal stopping theory to sub-dataset
         result = eulerStoppingTheory(monthlyData)

         #Creating entry in dict
         key = month + str(year)
         dict[key] = result

# Used to print dict in a readable form
#for key in dict.keys():
#   print(key)
#   print(dict[key])
#   print()
#

#4. 
# make graphs to visualize the price

#plt.fill_between(df2021['time'], df2021['priceUsd'], )
#plt.show()

#What we used:

#https://docs.coincap.io/
#https://www.youtube.com/watch?v=EoW4XFdh7gc