#!/usr/bin/env python3

# Import needed packages
import json
import requests
import csv
import re
import pandas as pd

# Documentation
# 'https://developer.foursquare.com/'
# 'https://developer.foursquare.com/docs/places-api/getting-started/'
# 'https://developer.foursquare.com/docs/api-reference/venues/explore/'

# Defining function




def getPlaces(LAT, LNG, QUERY):

    # Parameters for request
    url = 'https://api.foursquare.com/v2/venues/explore'
    LL = str(LAT) + ' ,' + str(LNG)
    params = dict(
        client_id="P0VECUSYDJB24CHOVK4SH1ZOS3ZC1VO00FZMIHNN0U1HMZT1",
        client_secret="RAKWBMTXSLUDEJZ53LABSEQFX1CX4E4VQ2RNF0JVFYBOZOZZ",
        v='20180323',
        ll=LL,
        query=QUERY,
        limit=1000
    )

    # Requesting data
    resp = requests.get(url=url, params=params)
    data = json.loads(resp.text)

    # Funneling JSON
    venues = data['response']['groups'][0]['items']

    # JSON to Tabular form
    nearby_venues = pd.json_normalize(venues)

    # # filter columns
    filtered_columns = ['venue.name', 'venue.location.lat', 'venue.location.lng', 'venue.location.formattedAddress', 'venue.categories']
    nearby_venues = nearby_venues.loc[:, filtered_columns]
    # nearby_venues = nearby_venues[filtered_columns]

    # Rename columns
    nearby_venues.columns = ['name', 'lat',  'lng', 'formattedAddress', 'categories']

    # Getting only the name of the cotegory
    for i in range(0, len(nearby_venues.categories)):
        nearby_venues.loc[i, "categories"] = str(re.search(
            "name(.*)pluralName", str(nearby_venues.categories[i])).group(1))[4:-4]

    0# Reordering the dataframe
    df = nearby_venues[['name', 'lat', 'lng', 'formattedAddress', 'categories']]

    # Convert it all to string
    df = df.astype(str)

    return df

# Function getManyPlaces to the location of many venues at different locations at once
def getManyPlaces(SEARCHPLACES, LOCATIONS):
    dff = pd.DataFrame(columns=['name', 'lat',  'lng', 'formattedAddress', 'categories'])
    for place in SEARCHPLACES:
        print("Searching for... "+place)
        for location in LOCATIONS:
            dff = dff.append(getPlaces(location[0], location[1], place))
    dff = dff.drop_duplicates()
    return dff
            

# Places of interest
SearchPlaces = ['Bakery', 'Bar', 'Bookstore', 'Gym', 'Design Studio', 'Shopping Mall', 'Lawyer', 'Boutique', 'Shop & Service', 'Factory', 'Clothing', 'Construction & Landscaping', 'Nail Salon', 'Airport', 'Market', 'Warehouse', 'Auto Garage', 'Electronics Store', 'Bank', 'Comic Shop', 'Shoe Store', 'Department Store', 'Shop', 'Automotive Shop', 'Supermarket', 'Furniture / Home Store', 'Insurance Office', 'Office', 'Health & Beauty Service', "Men's Store", 'Public Art', 'Pharmacy', 'Motorcycle Shop', 'Auto Workshop', 'University', 'Convenience Store', 'Drugstore', 'Hospital',
                'Clothing Store', 'Fruit & Vegetable Store', 'School', 'Stadium', 'Arts & Entertainment', 'Accessories Store', 'Tattoo Parlor', 'Newsstand', 'Food & Drink Shop', 'Financial or Legal Service', 'Bed & Breakfast', 'Mobile Phone Shop', 'Music Venue', 'Credit Union', 'Salon / Barbershop', 'Photography Studio', 'Business Service', 'Pet Service', 'ATM', 'Station', 'Restaurant', 'Gift shop', 'Performing Arts Venue', 'Gas Station', 'Terminal', "Women's Store", 'Entertainment Service', 'Store', 'Flower Shop', 'Cosmetics Shop', 'Ginásio', 'Grocery Store', 'Museum']
# SearchPlaces = ['Lawyer', 'Bar']
NotWorking = ['Motorsports Shop']

# Dictionary of locations of interest
dtLocations = {
    "mooca1": [-48.682939, -26.967448]
}

# dtLocations = centroids_bc.set_index('hexagon').T.to_dict('list')
# dtLocations['H001']


# Get the places of interest (Just 10 each time, It's better this way)
manyVenues0_10 = getManyPlaces(SearchPlaces[0:10], dtLocations.values())
manyVenues10_20 = getManyPlaces(SearchPlaces[10:20], dtLocations.values())
manyVenues20_30 = getManyPlaces(SearchPlaces[20:30], dtLocations.values())
manyVenues30_40 = getManyPlaces(SearchPlaces[30:40], dtLocations.values())
manyVenues40_50 = getManyPlaces(SearchPlaces[40:50], dtLocations.values())
manyVenues50_60 = getManyPlaces(SearchPlaces[50:60], dtLocations.values())
manyVenues60_70 = getManyPlaces(SearchPlaces[60:70], dtLocations.values())
manyVenues70_80 = getManyPlaces(SearchPlaces[70:80], dtLocations.values())

# Append them all together
manyVenues = pd.DataFrame(columns=['name', 'lat',  'lng', 'formattedAddress', 'categories'])
manyVenues = manyVenues.append([manyVenues0_10, manyVenues10_20, manyVenues20_30, manyVenues30_40, manyVenues40_50, manyVenues50_60, manyVenues60_70, manyVenues70_80])
manyVenues = manyVenues.drop_duplicates()

# Unique categories found in the dataset
manyVenues['categories'].unique()

# Get a variable 
manyVenues['categoria'] = manyVenues['categories']

manyVenues['categories'] = manyVenues['categories'].replace(['Shopping Mall', 'Shopping', 'Shopping Plaza'], 'Shopping')
manyVenues['categories'] = manyVenues['categories'].replace(['Hospital', 'Emergency Room', 'Medical Center', 'Medical Lab', 'Emergency Room'], 'Hospital')
manyVenues['categories'] = manyVenues['categories'].replace(['Pharmacy', 'Veterinarian', 'Acupuncturist', 'Doctor\'s Office', 'Drugstore'], 'Centro de saúde')
manyVenues['categories'] = manyVenues['categories'].replace(['Spa', 'Health & Beauty Service', 'Salon / Barbershop', 'Nail Salon', 'Massage Studio'], 'Centro de beleza')
manyVenues['categories'] = manyVenues['categories'].replace(['Supermarket', 'Big Box Store'], 'Supermercado')
manyVenues['categories'] = manyVenues['categories'].replace(['Grocery Store', 'Market', 'Farmers Market', 'Butcher', 'Fish Market', 'Food & Drink Shop', 'Food Service', 'Fruit & Vegetable Store', 'Health Food Store', 'Herbs & Spices Store', 'Organic Grocery', 'Warehouse Store'], 'Mercado')
manyVenues['categories'] = manyVenues['categories'].replace(['Coffee Shop', 'Acai House', 'Bagel Shop', 'Bakery', 'Breakfast Spot', 'Burger Joint', 'Café', 'Deli / Bodega', 'Diner', 'Food Court', 'Food Truck', 'Hot Dog Joint', 'Ice Cream Shop', 'Pastelaria', 'Sandwich Place', 'Snack Place', 'Airport Food Court', 'Creperie', 'Cupcake Shop', 'Dessert Shop', 'Donut Shop', 'Juice Bar', 'Street Food Gathering', 'Taco Place', 'Tea Room', 'Wings Joint'], 'Lanchonete')
manyVenues['categories'] = manyVenues['categories'].replace(['Airport', 'Bus Station', 'Bus Stop'], 'Transporte')
manyVenues['categories'] = manyVenues['categories'].replace(['Event Servic', 'Bus Station', 'Bus Stop', 'Design Studio', 'Entertainment Service', 'Home Service', 'IT Services', 'Tattoo Parlor', 'Other Repair Shop', 'Recording Studio', 'Shoe Repair', 'Pet Service', 'Photography Lab', 'Photography Studio', 'Event Service'], 'Serviço')
manyVenues['categories'] = manyVenues['categories'].replace(['American Restaurant', 'Argentinian Restaurant', 'Asian Restaurant', 'BBQ Joint', 'Bistro', 'Brazilian Restaurant', 'Buffet', 'Caribbean Restaurant', 'Chinese Restaurant', 'Churrascaria', 'Donburi Restaurant', 'Dumpling Restaurant', 'Eastern European Restaurant', 'Fast Food Restaurant', 'Fish & Chips Shop', 'Food', 'Fried Chicken Joint', 'German Restaurant', 'Italian Restaurant', 'Japanese Restaurant', 'Mediterranean Restaurant', 'Mexican Restaurant', 'Middle Eastern Restaurant', 'Mineiro Restaurant', 'Pizza Place', 'Portuguese Restaurant', 'Restaurant', 'Salad Place', 'Seafood Restaurant', 'Spanish Restaurant', 'Steakhouse', 'Sushi Restaurant', 'Swiss Restaurant', 'Vegetarian / Vegan Restaurant', 'Comfort Food Restaurant', 'French Restaurant', 'Gluten-free Restaurant', 'Gourmet Shop', 'Latin American Restaurant', 'Scandinavian Restaurant', 'Tapas Restaurant', 'Turkish Restaurant'], 'Restaurante')
manyVenues['categories'] = manyVenues['categories'].replace(['Athletics & Sports', 'Basketball Court', 'Basketball Stadium', 'Soccer Field', 'Soccer Stadium', 'Stadium', 'Tennis Court', 'Volleyball Court', 'Baseball Stadium', 'College Basketball Court', 'College Soccer Field', 'College Stadium', 'College Tennis Court', 'College Track', 'Football Stadium', 'Tennis Stadium', 'Track Stadium', 'Roller Rink', 'Go Kart Track'], 'Local para esporte')
manyVenues['categories'] = manyVenues['categories'].replace(['Automotive Shop', 'Electronics Store', 'Furniture / Home Store', 'Mobile Phone Shop', 'Paper / Office Supplies Store', 'Sporting Goods Shop', 'Accessories Store', 'Adult Boutique', 'Antique Shop', 'Arts & Crafts Store', 'Auto Garage', 'Auto Workshop', 'Board Shop', 'Bookstore', 'Boutique', 'Bridal Shop', 'Business Service', 'Candy Store', 'Cheese Shop', 'Chocolate Shop', 'Clothing Store', 'College Bookstore', 'Comic Shop', 'Construction & Landscaping', 'Convenience Store', 'Cosmetics Shop', 'Department Store', 'Flower Shop', 'Gas Station', 'Gift Shop', 'Hardware Store', 'Hobby Shop', 'Jewelry Store', 'Kids Store', 'Knitting Store', 'Leather Goods Store', 'Lingerie Store', 'Luggage Store', 'Men\'s Store', 'Miscellaneous Shop', 'Motorcycle Shop', 'Music Store', 'Newsstand', 'Optical Shop', 'Outdoor Supply Store', 'Outlet Store', 'Perfume Shop', 'Pet Store', 'Print Shop', 'Record Shop', 'Shoe Store', 'Shop & Service', 'Smoke Shop', 'Souvenir Shop', 'Stationery Store', 'Supplement Shop', 'Tailor Shop', 'Thrift / Vintage Store', 'Toy / Game Store', 'Used Bookstore', 'Watch Shop', 'Winery', 'Women\'s Store'], 'Loja')
manyVenues['categories'] = manyVenues['categories'].replace(['Bed & Breakfast', 'Hotel', 'Hostel'], 'Hotel')
manyVenues['categories'] = manyVenues['categories'].replace(['Bar', 'Beer Bar', 'Beer Garden', 'Brewery', 'Cocktail Bar', 'Dive Bar', 'Gastropub', 'Jazz Club', 'Karaoke Bar', 'Pool Hall', 'Pub', 'Sports Bar', 'Wine Bar', 'Wine Shop', 'Beer Store', 'Liquor Store', 'Strip Club'], 'Bar')
manyVenues['categories'] = manyVenues['categories'].replace(['Climbing Gym', 'College Gym', 'Cycle Studio', 'Dance Studio', 'Flight School', 'Gym', 'Gym / Fitness Center', 'Gym Pool', 'Gymnastics Gym', 'Martial Arts School', 'Pilates Studio', 'Yoga Studio'], 'Academia')
manyVenues['categories'] = manyVenues['categories'].replace(['Adult Education Center', 'Driving School', 'Elementary School', 'High School', 'Language School', 'Middle School', 'Music School', 'Nursery School', 'Preschool', 'Private School', 'Religious School', 'School', 'Student Center', 'Trade School'], 'Escola')
manyVenues['categories'] = manyVenues['categories'].replace(['College Lab', 'College Library', 'University', 'College Technology Building', 'Law School'], 'Universidade')
manyVenues['categories'] = manyVenues['categories'].replace(['Lawyer', 'Office', 'Coworking Space', 'Financial or Legal Service', 'Insurance Office', 'Tech Startup'], 'Escritório')
manyVenues['categories'] = manyVenues['categories'].replace(['ATM', 'Bank', 'Betting Shop', 'Credit Union', 'Currency Exchange', 'Lottery Retailer'], 'Banco ou lotérica')
manyVenues['categories'] = manyVenues['categories'].replace(['Other Nightlife', 'Concert Hall', 'Music Venue', 'Nightclub', 'Rock Club'], 'Casa noturna')
manyVenues['categories'] = manyVenues['categories'].replace(['Event Space', 'General Entertainment', 'Movie Theater', 'Museum', 'Other Nightlife', 'Performing Arts Venue', 'Art Museum', 'Art Gallery', 'Arts & Entertainment', 'Auditorium', 'Cultural Center', 'Escape Room', 'History Museum', 'Indie Movie Theater', 'Planetarium', 'Science Museum', 'Theater'], 'Local de eventos')
manyVenues['categories'] = manyVenues['categories'].replace(['Concert Hall', 'Historic Site', 'Memorial Site', 'Monument / Landmark', 'Outdoor Sculpture', 'Plaza'], 'Espaço público')
manyVenues['categories'] = manyVenues['categories'].replace(['Airport Gate', 'Airport Lounge', 'Airport Service', 'Airport Terminal', 'Bus Line', 'Light Rail Station', 'Metro Station', 'Plane', 'Platform', 'Residential Building (Apartment / Condo)', 'Road', 'Train', 'Train Station', 'Transportation Service', 'Bridge', 'Building', 'Festival', 'Flea Market', 'Garden', 'Garden Center', 'General Travel', 'Non-Profit', 'Public Art', 'Street Art'], 'remove')

# Remove the uninteresting ones
manyVenues = manyVenues[manyVenues['categories'] != 'remove']

# Rename the categories collumn to "tipo"]
manyVenues.columns

# Export as a .csv file
# manyVenues.to_csv(r'dfpontosdeinteresse.csv', index = False)

