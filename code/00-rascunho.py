#!/usr/bin/env python3

# Import needed packages
import json
import requests
import csv
import re
import pandas as pd
# from pymongo import MongoClient
# import pymongo

# Documentation
# 'https://developer.foursquare.com/'
# 'https://developer.foursquare.com/docs/places-api/getting-started/'
# 'https://developer.foursquare.com/docs/api-reference/venues/explore/'

SearchPlaces = ['Bakery', 'Bar', 'Bookstore', 'Gym', 'Design Studio', 'Shopping Mall', 'Lawyer', 'Boutique', 'Shop & Service', 'Factory', 'Clothing', 'Construction & Landscaping', 'Nail Salon', 'Airport', 'Market', 'Warehouse', 'Auto Garage', 'Electronics Store', 'Bank', 'Comic Shop', 'Shoe Store', 'Department Store', 'Shop', 'Automotive Shop', 'Supermarket', 'Furniture / Home Store', 'Insurance Office', 'Office', 'Health & Beauty Service', "Men's Store", 'Public Art', 'Pharmacy', 'Motorcycle Shop', 'Auto Workshop', 'University', 'Convenience Store', 'Drugstore', 'Hospital',
                'Clothing Store', 'Fruit & Vegetable Store', 'School', 'Stadium', 'Arts & Entertainment', 'Accessories Store', 'Tattoo Parlor', 'Newsstand', 'Food & Drink Shop', 'Financial or Legal Service', 'Bed & Breakfast', 'Mobile Phone Shop', 'Music Venue', 'Credit Union', 'Salon / Barbershop', 'Photography Studio', 'Business Service', 'Pet Service', 'ATM', 'Station', 'Restaurant', 'Gift shop', 'Performing Arts Venue', 'Gas Station', 'Terminal', "Women's Store", 'Entertainment Service', 'Store', 'Flower Shop', 'Cosmetics Shop', 'Ginásio', 'Grocery Store', 'Museum']
# SearchPlaces = ['Lawyer', 'Bar']
NotWorking = ['Motorsports Shop']
dtLocations = centroids_bc.set_index('hexagon').T.to_dict('list')
dtLocations['H001'][0]

# Parameters for request
url = 'https://api.foursquare.com/v2/venues/explore'
 
LL = str(dtLocations['H001'][1]) + ' ,' + str(dtLocations['H001'][0])
params = dict(
    client_id="P0VECUSYDJB24CHOVK4SH1ZOS3ZC1VO00FZMIHNN0U1HMZT1",
    client_secret="RAKWBMTXSLUDEJZ53LABSEQFX1CX4E4VQ2RNF0JVFYBOZOZZ",
    v='20180323',
    ll=LL,
    query='Automotive Shop',
    limit=1000
)

# Requesting data
resp = requests.get(url=url, params=params)

if int(resp.status_code)==200:
    print("okok")

data = json.loads(resp.text)

# Funneling JSON
venues = data['response']['groups'][0]['items']

if not venues:
  print("List is empty")

# JSON to Tabular form
nearby_venues=[]
nearby_venues = pd.json_normalize(venues)

# filter columns
filtered_columns = ['venue.name', 'venue.location.lat', 'venue.location.lng', 'venue.location.formattedAddress', 'venue.categories']
nearby_venues = nearby_venues.loc[:, filtered_columns]

# Rename columns
nearby_venues.columns = ['name', 'lat', 'lng', 'formattedAddress', 'categories']


bcup = nearby_venues
# nearby_venues = bcup

# Getting only the name of the cotegory
for i in range(0, len(nearby_venues.categories)):
    # print(nearby_venues.loc[i, "categories"])
    nearby_venues.loc[i, "categories"] = str(re.search("name(.*)pluralName", str(nearby_venues.categories[i])).group(1))[4:-4]

nearby_venues.loc[10, "categories"]

# Reordering the dataframe
df = nearby_venues[['name', 'lat', 'lng', 'formattedAddress', 'categories']]

# CORRIGIR FORMATTED ADDRESS

# Convert it all to string
df = df.astype(str)

# if VERIFIED == True => filter; else do nothing
# if int(resp.status_code)==200:
#     return df
# else: 
#     return None
return resp


getPlaces(-23.571460, -46.599977, "store")

