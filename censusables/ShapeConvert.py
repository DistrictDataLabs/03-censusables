import shapefile

# read the shapefile
reader = shapefile.Reader("/home/russ/Documents/DDL/Data/CensusShapeData/zipcode_files/tl_2014_us_zcta510.shp")
fields = reader.fields[1:]
field_names = [field[0] for field in fields]
buffer = []
print "Starting Reader..."
for sr in reader.shapeRecords():
    atr = dict(zip(field_names, sr.record))
    geom = sr.shape.__geo_interface__
    buffer.append(dict(type="Feature", \
    geometry=geom, properties=atr)) 

print "Staring Writer..."
# write the GeoJSON file
from json import dumps
geojson = open("zipcode.json", "w")
geojson.write(dumps({"type": "FeatureCollection",\
"features": buffer}, indent=2) + "\n")
geojson.close()

print "Finished"


