"""Parameters

the enclosing latitude and longitude points 

# of beds

type of listing (condo, co-op, etc.)

cost

square footage

change in price over 30 days
"""


# Before we hire at Compound, we ask that applicants complete a small task to demonstrate their work style to our team.
# 
# DATA SCIENCE PROJECT:  
# 
# Filtering Investment Opportunities
# At any given time, there are thousands of Manhattan residential condominiums listed for sale, and many more being quietly marketed through off-market transactions. By using our proprietary algorithm, we will winnow down the large list to the top 25 to 50 opportunities, those most likely to outperform. We want to focus our attention on those opportunities.
# 
# 
# Initially,
# - Must be condominium (not co-op or condop)  y
# - Must be able to rent out to a non-owner   x
# - Price: less than $3,500,000  y
# 
# - Price per square foot: less than $2,000 y
# 
# - Location: Manhattan south of 96th Street y 
# - Two and three bedroom apartments y 
# - Elevator or walk-up (but walk-up must be lower than 3rd floor)
# - Rental yield of 2pct or more (see below for calculation of rental yield)
# Create a exhausted list of all Manhattan listings that meet the above criteria, and generate a list of the top 30 investment opportunities in accordance with the criteria listed above. Propose how you would automatically update this list every week.
# Please send your questions and final work product to janine@getcompound.com

# In[1]:

#Dependencies
import pandas as pd
import zillow
from utils import inside_polygon, confirm_location

key = 'X1-ZWz1gk74zflatn_5jgqp'


# In[2]:

#The latitude and longitudinal points enclosing Manhattan, 96th street and below. 
p1 = [40.796,-73.975]
p2 = [40.783,-73.944]
p3 = [40.707,-74.029]
p4 = [40.701,-73.990]

points = [p1,p2,p3,p4]


api = zillow.ValuationApi()  #initialize zillow API. 


houses = pd.DataFrame([])  #start with this, can clean later on... 

nbeds = []
addresses = []
housekind = []
high_estimates = []
low_estimates = []
costs = []
sqfts = []
last_updated = []
cpss = []
dcost = []

import numpy as np
ints = np.arange(2000)
zpid0 = 244980000  #Starting house ID, going through 2000 of these. 
zpids = [x+zpid0 for x in ints] #create a list of all of them. 
for zpid in zpids:
    zpid = str(zpid)

    condo = confirm_location(zpid)  #plug into written function, confirms in Manhattan below 96th st. 

    if condo is not None: 
    #Now the listing has been confirmed as in this area, next up plug in address 
    #and zipcode to obtain deep search, and the relevant info. 
        
        address  = condo.full_address.street + ', ' +condo.full_address.city + ', ' +condo.full_address.state
        zipcode = condo.full_address.zipcode

        try:
            deep_condo = api.GetDeepSearchResults(key,address,zipcode)
            #This deep search provides all the other info for the listing, but not all of them are complete!
            house_info = deep_condo.extended_data
            condo_or = house_info.usecode
            beds = house_info.bedrooms   #string!
            cost = deep_condo.zestiamte.amount  #estimated price of it 
            delta_cost = deep_condo.zestiamte.amount_change_30days #how much the price has changed over the past 30 days. 
            sqft = float(deep_condo.extended_data.finished_sqft)
            high_estimate = condo.zestiamte.valuation_range_high
            low_estimate = condo.zestiamte.valuation_range_low
            cost_per_sqft = cost/sqft
            
            #Printing statements to track progress.
            #=print("Info of this listing:")
            #=print("address: ",address)
            #=print("What kind of house? ", condo_or)
            #=print("beds = ",beds)
            #=print("cost = ",cost)
            #=print("square footage = ",sqft)
            #=print("cost per sqft = ", cost_per_sqft)
            #space for separating next listing. 
            #=print(" ")
            addresses.append(address)
            nbeds.append(beds)
            housekind.append(condo_or)
            costs.append(cost)
            sqfts.append(sqft)
            cpss.append(cost_per_sqft)
            high_estimates.append(high_estimate)
            low_estimates.append(low_estimate)
            dcost.append(delta_cost)
            last_updated.append(condo.zestiamte.amount_last_updated)
            
        except:
            #This happens a lot. Demonstrates a larger problem with the website and/or software package used. 
            print("found a valid listing, but could not perform a zillow deep search")

            
#now create a database of available listings, to be further filtered below. 
houses['Address'] = addresses
houses['Beds'] = nbeds
houses['Type'] = housekind
houses['Cost'] = costs
houses['Square Footage'] = sqfts
houses['Cost Per Sq Ft'] = cpss
houses['Change in Price'] = dcost
houses['High Estimate'] = high_estimates
houses['Low Estimate'] = low_estimates
houses['Date Last Updated'] = last_updated


condos = houses.loc[houses['Type'] == 'Condominium']



#Create this new metric, range corresponding to uncertainty. 
condos['Estimate Range'] = condos['High Estimate'] - condos['Low Estimate']



condos.to_csv('Filtered Investment Opportunities.csv',path='../results/')

