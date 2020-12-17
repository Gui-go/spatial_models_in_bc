#!/usr/bin/env python3

import json
import requests
import csv
import re
import pandas as pd
import logging


# Documentation
# 'https://developer.foursquare.com/'
# 'https://developer.foursquare.com/docs/places-api/getting-started/'
# 'https://developer.foursquare.com/docs/api-reference/venues/explore/'


# Log config
LOG_FORMAT = "%(asctime)-24s [%(filename)s:%(lineno)d] \
    %(levelname)-6s %(message)s"
logging.basicConfig(filename='logs/logs.log',
                    filemode='a',
                    format=LOG_FORMAT,
                    level=logging.DEBUG)


class IntPoints:
    def __init__(self, lat, lng):
        self.places=['Bakery', 'Bar', 'Bookstore', 'Gym', 'Design Studio', 'Shopping Mall', 'Lawyer', 'Boutique', 'Shop & Service', 'Factory', 'Clothing', 'Construction & Landscaping', 'Nail Salon', 'Airport', 'Market', 'Auto Garage', 'Electronics Store', 'Bank', 'Comic Shop', 'Shoe Store', 'Department Store', 'Shop', 'Automotive Shop', 'Supermarket', 'Furniture / Home Store', 'Insurance Office', 'Office', 'Health & Beauty Service', "Men's Store", 'Public Art', 'Pharmacy', 'Motorcycle Shop', 'Auto Workshop', 'University', 'Convenience Store', 'Drugstore', 'Hospital', 'Clothing Store', 'Fruit & Vegetable Store', 'School', 'Stadium', 'Arts & Entertainment', 'Accessories Store', 'Tattoo Parlor', 'Newsstand', 'Food & Drink Shop', 'Financial or Legal Service', 'Bed & Breakfast', 'Mobile Phone Shop', 'Music Venue', 'Credit Union', 'Salon / Barbershop', 'Photography Studio', 'Business Service', 'Pet Service', 'ATM', 'Station', 'Restaurant', 'Gift shop', 'Performing Arts Venue', 'Gas Station', 'Terminal', "Women's Store", 'Entertainment Service', 'Store', 'Flower Shop', 'Cosmetics Shop', 'Ginásio', 'Grocery Store', 'Museum', 'Motorsports Shop']
        # not working = , 'Warehouse'
        # self.places = ['Bakery', 'Bar', 'Gym', 'Design Studio', 'Shopping Mall', 'Lawyer', 'Boutique', 'Shop & Service', 'Factory']
        self.url='https://api.foursquare.com/v2/venues/explore'
        self.latlong=f'{str(lat)} ,{str(lng)}',
        self.id="P0VECUSYDJB24CHOVK4SH1ZOS3ZC1VO00FZMIHNN0U1HMZT1",
        self.__secret="RAKWBMTXSLUDEJZ53LABSEQFX1CX4E4VQ2RNF0JVFYBOZOZZ",
        self.version='20180323',
        self.limit=1000
        logging.info('Class initialized')
    
    def setParam(self, place):
        self.query=place
        self.params = dict(
            client_id=self.id,
            client_secret=self.__secret,
            v=self.version,
            ll=self.latlong,
            query=self.query,
            limit=self.limit
        )
    
    def _req(self):
        self.req = requests.get(url=self.url, params=self.params)
        logging.info(self.req)

    def getDta(self):
        self.data = json.loads(self.req.text)
        logging.info('Got data')

    def getVenues(self):
        self.venues = self.data['response']['groups'][0]['items']
        logging.info('Venues gotten')

    def normalizeVenues(self):
        self.nearby_venues = pd.json_normalize(self.venues).loc[:, 
            ['venue.name', 'venue.location.lat', 'venue.location.lng', 'venue.location.formattedAddress', 'venue.categories']]
    
    def filterVenues(self):
        self.nearby_venues.columns = ['name', 'lat', 'lng', 'formattedAddress', 'categories']
        for i in range(0, len(self.nearby_venues.categories)):
            self.nearby_venues.loc[i, "categories"] = str(re.search(
                "name(.*)pluralName", str(self.nearby_venues.categories[i])).group(1))[4:-4]
        self.nearby_venues = self.nearby_venues[['name', 'lat', 'lng', 'formattedAddress', 'categories']]
        self.nearby_venues = self.nearby_venues.astype(str)

    def run(self):
        self.df = pd.DataFrame()
        for i in self.places:
            logging.info(f'Searching for {i}')
            self.setParam(place = i)
            self._req()
            self.getDta()
            self.getVenues()
            self.normalizeVenues()
            self.filterVenues()
            logging.info(f'More {self.nearby_venues.shape[0]} points of interest')
            self.df = self.df.append(self.nearby_venues)
            logging.info(f'{self.df.shape[0]} so far')
        self.df.drop_duplicates()
        logging.info(f'Total of {self.df.drop_duplicates().shape[0]} points of interest')


centroids_bc = pd.read_csv('data/centroids_bc.csv')
dtLocations = centroids_bc.set_index('hexagon').T.to_dict('list')
# dtLocations['H001'][1]
        

it = IntPoints(lat=dtLocations['H001'][1], lng=dtLocations['H001'][0])
it.run()
it.df
