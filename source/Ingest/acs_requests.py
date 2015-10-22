#!~/Envs/scratch/bin/python

import requests
import json
import sqlite3

class ACS:
    def __init__(self):
        self.api_url = 'http://api.census.gov/data/'
        self.api_year = '2013/acs3'
        self.api_key = '15d2d362b3b78eff40c9fbf432bc4e7d2c6a582b'


    def get_totalpopulation_msa(self):
        print 'Starting...'
        self.api_payload = {'get':'NAME,B01003_001E', 'for':'metropolitan statistical area/micropolitan statistical area', 'key': self.api_key}
        self.r = requests.get(self.api_url + self.api_year, params = self.api_payload)
        self.url = self.r.url
        self.status = str(self.r.status_code)
        print self.status + ":" + self.url
        self.results = self.r.json()
        self.conn = sqlite3.connect('/home/russ/Documents/DistrictDataLabs/Censusables/Databases/Censusables.db')

        for self.i, self.d in enumerate(self.results):
            #self.response_dict = self.results[i]
            #print self.response_dict['region_type_t']
            #print self.results['region_type_t']
            #print self.response_dict['region_code_t']
            #if self.response_dict['region_type_t'] == 'msa':
            if self.i == 0:
                continue
            else:
                self.keys = ( self.d[0]
                        ,'B01003_001E'
                        ,'Total Population'
                        ,'metropolitan statistical area/micropolitan statistical area'
                        ,self.d[1]
                        ,self.d[2]
                        ,'2011-2013'
                       )
                #print keys
                self.parameter_fill = ','.join('?' * len(self.keys))
                self.c = self.conn.cursor()
                self.c.execute("INSERT INTO 'ACS.TotalPopulation_MSA' (NAME, Variable_Name, Variable_Label, Geographic_Type, Population_Count, MSA_ID, Year) VALUES (%s)" % self.parameter_fill, self.keys)
                self.conn.commit()
                #print "Record:" + str(self.i)
        self.conn.close()
        print 'Finished'
        #with open ('B01003_001E_TotalPopulation.txt', 'w') as outfile:
        #    json.dump(self.results ,outfile)

    def get_totalpopulation_msa(self):
        print 'Starting...'
        self.api_payload = {'get':'NAME,B01003_001E', 'for':'metropolitan statistical area/micropolitan statistical area', 'key': self.api_key}
        self.r = requests.get(self.api_url + self.api_year, params = self.api_payload)
        self.url = self.r.url
        self.status = str(self.r.status_code)
        print self.status + ":" + self.url
        self.results = self.r.json()
        self.conn = sqlite3.connect('/home/russ/Documents/DistrictDataLabs/Censusables/Databases/Censusables.db')

        for self.i, self.d in enumerate(self.results):
            #self.response_dict = self.results[i]
            #print self.response_dict['region_type_t']
            #print self.results['region_type_t']
            #print self.response_dict['region_code_t']
            #if self.response_dict['region_type_t'] == 'msa':
            if self.i == 0:
                continue
            else:
                self.keys = ( self.d[0]
                        ,'B01003_001E'
                        ,'Total Population'
                        ,'metropolitan statistical area/micropolitan statistical area'
                        ,self.d[1]
                        ,self.d[2]
                        ,'2011-2013'
                       )
                #print keys
                self.parameter_fill = ','.join('?' * len(self.keys))
                self.c = self.conn.cursor()
                self.c.execute("INSERT INTO 'ACS.TotalPopulation_MSA' (NAME, Variable_Name, Variable_Label, Geographic_Type, Population_Count, MSA_ID, Year) VALUES (%s)" % self.parameter_fill, self.keys)
                self.conn.commit()
                #print "Record:" + str(self.i)
        self.conn.close()
        print 'Finished'
        #with open ('B01003_001E_TotalPopulation.txt', 'w') as outfile:
        #    json.dump(self.results ,outfile)

        
 
if __name__ == '__main__':
    g = ACS()
    g.get_totalpopulation()
    #print g.results

#C-u C-c C-c
