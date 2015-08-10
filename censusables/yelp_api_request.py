#!~/Envs/scratch/bin/python

import requests
import json
import sqlite3
from pprint import pprint

class Yelp:
    def __init__(self):
        self.api_url = 'http://api.yelp.com'

    def get_businessdata_db (self):
        print 'Starting...'

        self.conn = sqlite3.connect('/home/russ/Documents/DistrictDataLabs/Projects/03-censusables/databases/Censusables.db')
        self.c = self.conn.cursor()
        self.c.execute ("SELECT name FROM sqlite_master WHERE type='table' AND name='Yelp.Businesses';")
        self.row = self.c.fetchone()
        if self.row is None:
            self.c.execute("""
                           CREATE TABLE "Yelp.Businesses" (row_id INTEGER PRIMARY KEY AUTOINCREMENT, type CHAR (255), business_id CHAR (255), name CHAR (255), 
                           neighborhoods CHAR (4000), full_address CHAR (255), city CHAR (100), state CHAR (100), latitude REAL, longitude REAL, stars REAL, 
                           review_count INTEGER, categories CHAR (4000), open BOOLEAN, hours CHAR (4000), attributes CHAR (4000));
                           """)
        self.count = 1
        with open ('/home/russ/Documents/DistrictDataLabs/Censusables/Yelp DataSet/yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_business.json') as businessfile:
            for line in businessfile:
                self.d = json.loads(line)
                self.keys = ( ((self.d['type'],) if 'type' in self.d else (None,)) +
                        ((self.d['business_id'],) if 'business_id' in self.d else (None,))+
                        ((self.d['name'],) if 'name' in self.d else (None,)) +
                        ((str(self.d['neighborhoods']),) if 'neighborhoods' in self.d else (None,)) +
                        ((self.d['full_address'],) if 'full_address' in self.d else (None, )) +
                        ((self.d['city'],) if 'city' in self.d else (None,)) +
                        ((self.d['state'],) if 'state' in self.d else (None,)) +
                        ((self.d['latitude'],) if 'latitude' in self.d else (None,)) +
                        ((self.d['longitude'],) if 'longitude' in self.d else (None,)) +
                        ((self.d['stars'],) if 'stars' in self.d else (None,)) +
                        ((self.d['review_count'],) if 'review_count' in self.d else (None,)) +
                        ((str(self.d['categories']),) if 'categories' in self.d else (None,)) +
                        ((self.d['open'],) if 'open' in self.d else (None,)) +
                        ((str(self.d['hours']),) if 'hours' in self.d else (None,)) +
                        ((str(self.d['attributes']),) if 'attributes' in self.d else (None,))
                        )
                self.c = self.conn.cursor()
                self.parameter_fill = ','.join('?' * len(self.keys))
                self.c.execute("""
                              INSERT INTO 'Yelp.Businesses' (type, business_id, name, neighborhoods, full_address, city, state, latitude, longitude, 
                                     stars, review_count, categories, open, hours, attributes)
                                     VALUES (%s)
                              """ % self.parameter_fill, self.keys)
                self.conn.commit()
                print 'Record: ' + str(self.count)
                self.count += 1
        self.conn.close()
        print 'Finished.'

    def get_reviewdata_db (self):
        print 'Starting...'

        self.conn = sqlite3.connect('/home/russ/Documents/DistrictDataLabs/Projects/03-censusables/databases/Censusables.db')
        self.c = self.conn.cursor()
        self.c.execute ("SELECT name FROM sqlite_master WHERE type='table' AND name='Yelp.Reviews';")
        self.row = self.c.fetchone()
        if self.row is None:
            self.c.execute("""
                           CREATE TABLE "Yelp.Reviews" (row_id INTEGER PRIMARY KEY AUTOINCREMENT, type CHAR (255), user_id CHAR (255), stars REAL, text CHAR (8000),                           date DATETIME, votes CHAR (4000));
                           """)
        #self.count = 1
        with open ('/home/russ/Documents/DistrictDataLabs/Censusables/Yelp DataSet/yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_review.json') as reviewfile:
            for line in reviewfile:
                self.d = json.loads(line)
                self.keys = ( ((self.d['type'],) if 'type' in self.d else (None,)) +
                        ((self.d['user_id'],) if 'user_id' in self.d else (None,))+
                        ((self.d['stars'],) if 'stars' in self.d else (None,)) +
                        ((self.d['text'],) if 'text' in self.d else (None,)) +
                        ((self.d['date'],) if 'date' in self.d else (None, )) +
                        ((str(self.d['votes']),) if 'votes' in self.d else (None,)) 
                        )
                self.c = self.conn.cursor()
                self.parameter_fill = ','.join('?' * len(self.keys))
                self.c.execute("""
                              INSERT INTO 'Yelp.Reviews' (type, user_id, stars, text, date, votes)
                                     VALUES (%s)
                              """ % self.parameter_fill, self.keys)
                self.conn.commit()
                #print 'Record: ' + str(self.count)
                #self.count += 1
        self.conn.close()
        print 'Finished.'

    def get_reviewdata_file (self):
        print 'Starting...'
        with open ('/home/russ/Documents/DistrictDataLabs/Censusables/Yelp DataSet/yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_review.json') as reviewfile:
            for line in reviewfile:
                self.d = json.loads(line)
                self.keys = ( ((self.d['type'],) if 'type' in self.d else (None,)) +
                        ((self.d['user_id'],) if 'user_id' in self.d else (None,))+
                        ((self.d['stars'],) if 'stars' in self.d else (None,)) +
                        ((self.d['text'],) if 'text' in self.d else (None,)) +
                        ((self.d['date'],) if 'date' in self.d else (None, )) +
                        ((str(self.d['votes']),) if 'votes' in self.d else (None,)) 
                        )
                self.c = self.conn.cursor()
                self.parameter_fill = ','.join('?' * len(self.keys))
                self.c.execute("""
                              INSERT INTO 'Yelp.Reviews' (type, user_id, stars, text, date, votes)
                                     VALUES (%s)
                              """ % self.parameter_fill, self.keys)
                self.conn.commit()
                print 'Record: ' + str(self.count)
                self.count += 1
        self.conn.close()
        print 'Finished.'


    def get_userdata_db (self):
        print 'Starting...'

        self.conn = sqlite3.connect('/home/russ/Documents/DistrictDataLabs/Projects/03-censusables/databases/Censusables.db')
        self.c = self.conn.cursor()
        self.c.execute ("SELECT name FROM sqlite_master WHERE type='table' AND name='Yelp.Users';")
        self.row = self.c.fetchone()
        if self.row is None:
            self.c.execute("""
                           CREATE TABLE "Yelp.Users" (row_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id CHAR (255), name CHAR (255), review_count INTEGER, average_                           stars REAL, votes CHAR (4000), friends CHAR (8000), elite REAL, yelping_since DATETIME, compliments CHAR (8000), fans INTEGER);
                           """)
        #self.count = 1
        with open ('/home/russ/Documents/DistrictDataLabs/Censusables/Yelp DataSet/yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_review.json') as userfile:
            for line in userfile:
                self.d = json.loads(line)
                self.keys = ( ((self.d['type'],) if 'type' in self.d else (None,)) +
                        ((self.d['user_id'],) if 'user_id' in self.d else (None,))+
                        ((self.d['stars'],) if 'stars' in self.d else (None,)) +
                        ((self.d['text'],) if 'text' in self.d else (None,)) +
                        ((self.d['date'],) if 'date' in self.d else (None, )) +
                        ((self.d['votes'],) if 'votes' in self.d else (None,)) 
                        )
                self.c = self.conn.cursor()
                self.parameter_fill = ','.join('?' * len(self.keys))
                self.c.execute("""
                              INSERT INTO 'Yelp.Review' (type, user_id, stars, text, date, votes)
                                     VALUES (%s)
                              """ % self.parameter_fill, self.keys)
                self.conn.commit()
                #print 'Record: ' + str(self.count)
                #self.count += 1
        self.conn.close()
        print 'Finished.'

def main():
    y = Yelp()
    #y.get_businessdata_db()
    y.get_reviewdata_db()
    #y.get_userdata_db()
        
 
if __name__ == '__main__':
    main()
#C-u C-c C-c
