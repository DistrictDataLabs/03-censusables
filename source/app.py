#!~/anaconda/bin/ python
# -*- coding: utf-8 -*-

################################################################################
# Imports
################################################################################

import data
import json
import csv
import vincent
from vincent import AxisProperties, PropertySet, ValueRef
from flask import Flask, render_template, request
app = Flask(__name__)

################################################################################
# Globals
################################################################################


Final_File = "Data/final_files/Final.csv"
Map_Init =  "static/USA_Init_Map.json"
Map_States = "static/us_states.topo.json"
Map_StateMap_Path =  "static/states_topo_json/"
Map_Zips =  "static/zips_us_topo.json"
State_LandArea = r"Data/raw_files/state_landarea_rank.csv"

#Read final DataFrame
df_final = data.df_final

#Read State Land Area
with open(State_LandArea) as f:
    f.readline() # ignore first line (header)
    land_area = dict(csv.reader(f, delimiter=','))


################################################################################
# Routes
################################################################################


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/data/map")
def data_map():
    return_dict = {}
    income = request.args.get("income")
    housing = request.args.get("housing")
    diversity = request.args.get("diversity")
    urbanization = request.args.get("urbanization")
    state = request.args.get("state")
    statename = request.args.get("statename").replace(" ","_")

    global df_final
    fit = []
    fit.append(float(income)/100)
    fit.append(float(housing)/100)
    fit.append(float(diversity)/100)
    fit.append(float(urbanization)/100)        
    df_final['fit'] = df_final.apply(lambda x: abs(fit[0]-x['diversity_index'])+abs(fit[1]-x['housing_index'])+abs(fit[2]-x['income_index'])+abs(fit[3]-x['urban_index']),axis=1)

    if state == 'ZZ':
        zip_topo = r'/data/zips'
        state_topo = r'/data/states'

        geo_data = [{'name': 'states',
                     'url': state_topo,
                     'feature': 'us_states.geo'},
                    {'name': 'zip_codes',
                     'url': zip_topo,
                     'feature': 'zip_codes_for_the_usa'}]

        vis = vincent.Map(data=df_final, geo_data=geo_data, scale=800, projection='albersUsa',
                          data_bind='fit', data_key='zip5',brew='YlOrRd',
                          map_key={'zip_codes': 'properties.zip'})
        del vis.marks[0].properties.update
        vis.marks[1].properties.enter.stroke_opacity = ValueRef(value=0.05)
        vis.marks[0].properties.enter.stroke.value = '#C0C0C0'

        vis.legend(title='Preferred ZipCode')
        return_dict[0] = json.loads(vis.to_json())
        
        ziplist = json.loads(df_final[['ZCTA5','ZIPName','fit']].sort(['fit']).reset_index().head(5).to_json())
        table_data = []
        for i in range (5):
            dict_row = {}
            dict_row['index'] = i
            dict_row['ZCTA5'] = ziplist['ZCTA5'][str(i)]
            dict_row['ZIPName'] = ziplist['ZIPName'][str(i)]
            table_data.append(dict_row)
        return_dict[1] = table_data
        #with open ('data.json','w') as outfile:
        #    json.dump(lst,outfile)

        return json.dumps(return_dict)

    
    else:
        zip_topo = r'/data/state_map?state='+statename
        feature_name = statename+r'.geo'

        global land_area
        rank = int(land_area[statename])
        if rank > 0 and rank <=1:
            scale = 700
        elif rank >1 and rank <=3: 
            scale = 2500
        elif rank >2 and rank <=19: 
            scale = 3000
        elif rank >19 and rank <=26: 
            scale = 4000
        elif rank >26 and rank <=39: 
            scale = 4500
        elif rank >39 and rank <=40:
            scale = 5000
        elif rank >40 and rank <=48:
            scale = 6000
        else:
            scale = 23000


        geo_data = [{'name': 'state',
                     'url': zip_topo,
                     'feature': feature_name},
                     {'name': 'zip_codes',
                     'url': zip_topo,
                     'feature': feature_name}]

        vis = vincent.Map(data=df_final[df_final['State']==state],geo_data=geo_data, scale=scale, projection='equirectangular',
                          data_bind='fit', data_key='zip5',brew='YlOrRd',
                          map_key={'zip_codes': 'id'})

        del vis.marks[0].properties.update
        #vis.marks[0].properties.enter.stroke.value = '#C0C0C0'
        vis.marks[1].properties.enter.stroke_opacity = ValueRef(value=0.5)
        #vis.legend(title='Preferred ZipCode')
        return_dict[0] = json.loads(vis.to_json())

        ziplist = json.loads(df_final[['ZCTA5','ZIPName','fit']][df_final['State']==state].sort(['fit']).reset_index().head(5).to_json())
        table_data = []
        for i in range (5):
            dict_row = {}
            dict_row['index'] = i
            dict_row['ZCTA5'] = ziplist['ZCTA5'][str(i)]
            dict_row['ZIPName'] = ziplist['ZIPName'][str(i)]
            table_data.append(dict_row)
        return_dict[1] = table_data

        return json.dumps(return_dict)

@app.route("/data/init")
def data_init():
    json_data=open(Map_Init).read()
    data = json.loads(json_data)
    return json.dumps(data)

@app.route("/data/states")
def data_states():
    json_data=open(Map_States).read()
    data = json.loads(json_data)
    return json.dumps(data)

@app.route("/data/zips")
def data_zips():
    json_data=open(Map_Zips).read()
    data = json.loads(json_data)
    return json.dumps(data)

@app.route("/data/state_map")
def data_state_map():
    state = request.args.get("state")
    
    map_name = Map_StateMap_Path + state + ".topo.json"
    json_data=open(map_name).read()
    data = json.loads(json_data)
    return json.dumps(data)


################################################################################
# Main Execution
################################################################################

if __name__ == "__main__":
    app.run(debug=True)
