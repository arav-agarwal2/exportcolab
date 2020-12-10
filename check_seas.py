import json
from shapely.geometry import shape, GeometryCollection
import shapely.geometry
from shapely.geometry.polygon import Polygon
from shapely.geometry.point import Point
import geojson

with open("earth-seas-1m.geo.json") as f:
    features = geojson.load(f)
    poly = shape(features)

def pointInSea(lat, lon):
    return poly.contains(Point(lat,lon))

def trajectoryIntersectCoast(trajectory):
    return poly.intersects( shapely.geometry.LineString(trajectory))

def getIntersectionPoint(trajectory):
    ls = shapely.geometry.LineString(trajectory)
    print(ls)
    return poly.intersection(shapely.geometry.LineString(trajectory))

if __name__ == "__main__":
    print(pointInSea(56.8,-26.7))
