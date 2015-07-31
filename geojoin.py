"""Do a geographical join between a JSON data file and a Census shape file.

I used the anacondan distribution abd used conda to install:

- gdal
- shapely
- pyproj

"""
import argparse
import json
import osgeo.ogr
import pyproj
import shapely.geometry
import shapely.wkt


parser = argparse.ArgumentParser(__doc__)
parser.add_argument("shapefile", help="Census shape (.shp) file")

datafile_help = """JSON line-delimeted data file

Each line contains a data record. Each record must have latitude and
longitude properties.
"""
parser.add_argument("datafile", help=datafile_help)
parser.add_argument("output", help="Name of JSON line-delimited output file")
parser.add_argument('-s', '--shape-field', action='append')
parser.add_argument('-d', '--data-field', action='append')

# XXX later attribute names for geoid and name are different for state
# and county layers.  The later have a '10' suffix. WTF?

def main():
    args = parser.parse_args()
    if not args.shapefile.endswith('.shp'):
        args.shapefile += '.shp'
    geo = osgeo.ogr.Open(args.shapefile)
    assert geo.GetLayerCount() == 1
    layer = geo.GetLayer(0)
    proj = pyproj.Proj(layer.GetSpatialRef().ExportToProj4())
    features = []
    print('gathering features')
    for i in range(layer.GetFeatureCount()):
        feature = layer.GetFeature(i)
        shape_fields = dict((name, feature[name]) for name in args.shape_field)
        geometry = shapely.wkt.loads(feature.GetGeometryRef().ExportToWkt())
        features.append((shape_fields, geometry))

    print('joining')
    with open(args.output, 'w') as output:
        with open(args.output+'.failed', 'w') as failed:
            with open(args.datafile) as datafile:
                for line in datafile:
                    data = json.loads(line)
                    p = shapely.geometry.Point(
                        *proj(data['longitude'], data['latitude']))
                    for shape_fields, geometry in features:
                        if geometry.contains(p):
                            outd = shape_fields.copy()
                            outd.update((name, data[name])
                                        for name in args.data_field)
                            output.write(json.dumps(outd)+'\n')
                            break
                    else:
                        failed.write(json.dumps(data)+'\n')

if __name__ == '__main__':
    main()
