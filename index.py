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

#==============================================================================================================================
########################### ONLY USED ONCE TO STORE SPECIFC DATA LOCALLY ################################################################################
#Use CoinCap API to request historical data
#url = 'http://api.coincap.io/v2/assets/bitcoin/history?interval=d1'#&start=1592585794000&end=1613753794000' #can we use a variable for the unix time 1592585794000 ? 1613753794000

#payload = {}
#headers = {}

#response = requests.request("GET", url, headers=headers, data=payload)

#json_data = json.loads(response.text.encode('utf8'))
#bitcoin_data = json_data["data"]

# create pandas dataframe and save to csv file
#df = pd.DataFrame(bitcoin_data)
#df.to_csv('bitcoin-data', index=False)
########################### ONLY USED ONCE TO STORE SPECIFC DATA LOCALLY ################################################################################

#==============================================================================================================================

#Supressing SettingWithCopyWarning
pd.options.mode.chained_assignment = None  # default='warn'

def convertFromUnixTimeToDateTime(unixTime):
   return datetime.utcfromtimestamp(unixTime/1000).strftime('%m%d%Y')

def extractDate(dte):
   return dte[:10]

def getWeekday(dte):
   weekday = {
      0:"Monday",
      1:"Tuesday",
      2:"Wednesday",
      3:"Thursday",
      4:"Friday",
      5:"Saturday",
      6:"Sunday",
   }

   year, month, day = dte.split('-')

   obtainedWeekday = date(int(year), int(month), int(day)).weekday()

   return weekday.get(obtainedWeekday, None)

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
################
   for max in testDf['priceUsd']: # IS THIS LOOKING FOR THE PERCENT DIFFERENCE BETWEEN DAYS? IT CANT JUST BE THE NOMINAL VALUE OF THE PRICE <--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
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
################


#Creating dataframe that stores data [priceUSD, time, date] from website to pandas dataframe
df = pd.read_csv('bitcoin-data')
#pprint.pprint(df)
################

################
# create an excel file from the csv file
filename = 'bitcoin_historical_price_spreadsheet' + '.xlsx'
df.to_excel(filename)

# read the excel data
df_excel = pd.read_excel(filename, engine='openpyxl',)
################

# make a price chart using matplotlib
plt.title('Bitcoin Price')

plt.xticks(rotation=70)
plt.legend('legend')

plt.plot(df_excel['priceUsd'])
plt.ylabel('Price')

#plt.xlabel('Days (starting August 2019')
plt.show()

#Saving the chart into a JPG file
plt.savefig('bitcoin_historical_price_chart.png', bbox_inches='tight')

################


#Convert time values from Unix Time to datatime [Month Day Year]
df['time'] = df['time'].apply(convertFromUnixTimeToDateTime)

#Adding new column that stores what month the piece of data is from
df['month'] = df['time'].apply(assignMonth)

#Extracts the date (first 10 characters) from the date column and stores that value in the column
df['extractedDate'] = df['date'].apply(extractDate)

#Stores the what day of the week it is based on the date
df['weekday'] = df['extractedDate'].apply(getWeekday)

################
# add column that stores the day <----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
################

monthlyData = None
months = {"August", "September", "October", "November", "December", "January", "February", "March", "April", "May", "June", "July"}

################
# Create a starburst graph of the percent values of each day <--------------------------------------------------------------------------------------------------------------------------------
# like this:
# Crypto, Name, Algorithm, Quantity, USD_Price, USD_Value, BTC_Value, Percent = df['Crypto'], df['Name'], df['Algorithm'], df['Quantity'], df['USD Price'], df['USD Value'], df['BTC Value'], df['Percent']

#the visualization part 
# fig = px.sunburst(df, path = [Crypto, Name, Percent], values = Percent, color = df['USD Value'], title = 'Portfolio')
# fig.show()

#save to file called "Crypto_Sunburst(today's date)"
# plotly.offline.plot(fig, filename = 'Crypto_Sunburst' + str(today) + '.html')
##################

3. 
# make separate file with the Euler game theory strategy. 

#Initializing container to store results of applying optimal stopping theory
# Key is the MonthYear
# Value is an array that contains a list of values (list of values listed in eulerStoppingTheory method)
dict = {}
################## 
# Create an Excel file of this <-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
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
##################

#print the dictionary
#pprint.pprint(dict)

################
# mention results for March and April 2020 (COVID lockdowns)  <-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
################

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