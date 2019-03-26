#!/usr/bin/env python

# make sure to install these packages before running:
# pip install pandas
# pip install sodapy

import pandas as pd
from sodapy import Socrata
from geojson import LineString
from geojson import Feature
from geojson import FeatureCollection
from geojson import dump

# Unauthenticated client only works with public data sets. Note 'None'
# in place of application token, and no username or password:
client = Socrata("data.cityofnewyork.us", None)

# Example authenticated client (needed for non-public datasets):
# client = Socrata(data.cityofnewyork.us,
#                  MyAppToken,
#                  userame="user@example.com",
#                  password="AFakePassword")

# First 2000 results, returned as JSON from API / converted to Python list of
# dictionaries by sodapy.
results = client.get("i4gi-tjb9", limit=100000)

max = 1000000
fields = ['id', 'speed', 'travel_time', 'status', 'data_as_of', 'link_id', 'link_points', 'owner', 'transcom_id', 'borough', 'link_name']
# Convert to pandas DataFrame
results_df = pd.DataFrame.from_records(results)

features = []
for index, row in results_df.iterrows():
    properties = {}
    for field in fields:
        key = field
        value = row[key]
        properties[key] = value
    coord_text = row.link_points
    coord_list = coord_text.split(' ')
    coords = []
    for l in coord_list:
        pair = l.split(',')
        try:
            tuple(map(float, pair))
        except:
            print("Error: In Coordinates: %s" % (pair))
        else:
            pair = tuple(map(float, pair))
            if len(pair) > 1:
                pair = pair[::-1]
                coords.append(pair)
            else:
                print('Error: Coordinates are incomplete %s ' % pair)

    linestring = LineString(coords)

    features.append(Feature(geometry=linestring, properties=properties))

    if index > max:
        break


feature_collection = FeatureCollection(features)
with open('output/test.geojson', 'w') as f:
    dump(feature_collection, f)