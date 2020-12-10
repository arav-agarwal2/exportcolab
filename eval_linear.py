import pandas as pd
import numpy as np
import json
from shapely.geometry import shape, GeometryCollection
import shapely.geometry
from shapely.geometry.polygon import Polygon
from shapely.geometry.point import Point
import geojson


VEHICLECLASS = 0

data = pd.read_csv(str(VEHICLECLASS)+".csv", header=None,names=["MMSI", "TimeDate", "LAT","LON", "SOG","COG","Heading","Name","IMO","CallSign","VesselType","Status","Length","Width","Draft","Cargo","TranscieverClass"])
data["TimeDate"] = pd.to_datetime(data["TimeDate"]).apply(lambda x: x.timestamp())
data = data.groupby("MMSI").apply(np.array)
data = data.reset_index()


with open("earth-seas-1m.geo.json") as f:
    features = geojson.load(f)
    poly = shape(features)



def trajectoryIntersectCoast(trajectory, poly):
    return poly.intersects( shapely.geometry.LineString(trajectory))

def getIntersectionPoint(trajectory,poly):
    return poly.intersection(shapely.geometry.LineString(trajectory))



def data_iterator(myarray):
    for row in data[0]:
        item = np.transpose(row)
        time = list(item[1])
        lat = list(item[2])
        lon = list(item[3])
        yield (time,lat,lon)

count = 0
amount = 0
for element in data_iterator(data):
    time,lat,lon = element
    test = list(zip(lat,lon))
    count += 1
    print(count)
    if(trajectoryIntersectCoast(test,poly)):
        amount += 1
print(amount/count)
