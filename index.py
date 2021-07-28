
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


#1. 
# Get data. https://datahub.io/cryptocurrency/bitcoin#pandas
from datapackage import Package

package = Package('https://datahub.io/cryptocurrency/bitcoin/datapackage.json')

# print list of all resources:
pprint.pprint(package.resource_names)

# print processed tabular data (if exists any)
for resource in package.resources:
    if resource.descriptor['datahub']['type'] == 'derived/csv':
        pprint.pprint(resource.read())
 
#2. 
# make pandas dataframe

#3. 
# make individual graphs of last hour, day, month, and year. 

#4. 
# make separate file with the Euler game theory strategy. 

#5. 
# Make seperate file with the results of the strat vs. (buy and hold). 

#6. 
# makeI think .chart() might work idk

