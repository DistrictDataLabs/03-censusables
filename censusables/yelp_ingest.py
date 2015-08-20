#!~/Envs/scratch/bin/python

import requests
import json
import sqlite3
from pprint import pprint

class Yelp:
    def __init__(self):
        self.api_url = 'http://api.yelp.com'
        self.location_db = '/home/russ/Documents/DDL/Projects/03-censusables/databases/Censusables.db'
        self.location_file_businesses = '/home/russ/Documents/DDL/Data/YelpData/yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_business.json'
        self.location_file_reviews = '/home/russ/Documents/DistrictDataLabs/Censusables/Yelp DataSet/yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_review.json'
        self.location_file_users = '/home/russ/Documents/DistrictDataLabs/Censusables/Yelp DataSet/yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_user.json'

    def get_businessdata_to_db (self):
        print 'Starting...'

        self.conn = sqlite3.connect(self.location_db)
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
        with open (self.location_file_businesses) as businessfile:
            for line in businessfile:
                self.d = json.loads(line)
                self.values = ( ((self.d['type'],) if 'type' in self.d else (None,)) +
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
                self.parameter_fill = ','.join('?' * len(self.values))
                self.c.execute("""
                              INSERT INTO 'Yelp.Businesses' (type, business_id, name, neighborhoods, full_address, city, state, latitude, longitude, 
                                     stars, review_count, categories, open, hours, attributes)
                                     VALUES (%s)
                              """ % self.parameter_fill, self.values)
                self.conn.commit()
                print 'Record: ' + str(self.count)
                self.count += 1
        self.conn.close()
        print 'Finished.'

    def get_reviewdata_to_db (self):
        print 'Starting...'

        self.conn = sqlite3.connect(self.location_db)
        self.c = self.conn.cursor()
        self.c.execute ("SELECT name FROM sqlite_master WHERE type='table' AND name='Yelp.Reviews';")
        self.row = self.c.fetchone()
        if self.row is None:
            self.c.execute("""
                           CREATE TABLE "Yelp.Reviews" (row_id INTEGER PRIMARY KEY AUTOINCREMENT, type CHAR (255), business_id CHAR (255), user_id CHAR (255), stars REAL, text CHAR (8000),                           date DATETIME, votes CHAR (4000));
                           """)
        else:
            print "Table Yelp.Reviews already exists. Checking for existing user_id's."
        self.c.execute ("SELECT user_id, business_id FROM 'Yelp.Reviews'")
        self.existing_records = self.c.fetchall()
        print "There are " + str(len(self.existing_records)) + " existing reviews"
        self.headers = ['type'
                       ,'business_id'
                       ,'user_id'
                       ,'stars'
                       ,'text'
                       ,'date'
                       ,'votes']
        with open (self.location_file_reviews) as reviewfile:
            for i, line in enumerate(reviewfile):
                if i <= 1389720:
                    continue
                self.d = json.loads(line)
                self.values = ( ((self.d['type'],) if 'type' in self.d else (None,)) +
                        ((self.d['business_id'],) if 'business_id' in self.d else (None,)) +
                        ((self.d['user_id'],) if 'user_id' in self.d else (None,)) +
                        ((self.d['stars'],) if 'stars' in self.d else (None,)) +
                        ((self.d['text'],) if 'text' in self.d else (None,)) +
                        ((self.d['date'],) if 'date' in self.d else (None, )) +
                        ((str(self.d['votes']),) if 'votes' in self.d else (None,)) 
                        )
                self.value_ids = (((self.d['business_id'],) if 'business_id' in self.d else (None,)) +
                        ((self.d['user_id'],) if 'user_id' in self.d else (None,)))
                if self.value_ids in self.existing_records:
                    print str(i) + ': Already Exists'
                    continue
                else:
                    self.parameter_fill = ','.join('?' * len(self.headers))
                    self.c.execute("""
                              INSERT INTO 'Yelp.Reviews' (type, user_id, business_id, stars, text, date, votes)
                                     VALUES (%s)
                              """ % self.parameter_fill, self.values)
                    self.conn.commit()
                    print i
        self.conn.close()
        print 'Finished.'

    def get_reviewdata_file (self):
        print 'Starting...'
        with open (self.location_file_reviews) as reviewfile:
            for line in reviewfile:
                self.d = json.loads(line)
                self.values = ( ((self.d['type'],) if 'type' in self.d else (None,)) +
                        ((self.d['business_id'],) if 'business_id' in self.d else (None,))+
                        ((self.d['user_id'],) if 'user_id' in self.d else (None,))+
                        ((self.d['stars'],) if 'stars' in self.d else (None,)) +
                        ((self.d['text'],) if 'text' in self.d else (None,)) +
                        ((self.d['date'],) if 'date' in self.d else (None, )) +
                        ((str(self.d['votes']),) if 'votes' in self.d else (None,)) 
                        )
                self.c = self.conn.cursor()
                self.parameter_fill = ','.join('?' * len(self.values))
                self.c.execute("""
                              INSERT INTO 'Yelp.Reviews' (type, business_id, user_id, stars, text, date, votes)
                                     VALUES (%s)
                              """ % self.parameter_fill, self.values)
                self.conn.commit()
                print 'Record: ' + str(self.count)
                self.count += 1
        self.conn.close()
        print 'Finished.'


    def get_userdata_to_db (self):
        print 'Starting...'

        self.conn = sqlite3.connect(self.location_db)
        self.c = self.conn.cursor()
        self.c.execute ("SELECT name FROM sqlite_master WHERE type='table' AND name='Yelp.Users';")
        self.row = self.c.fetchone()
        if self.row is None:
            self.c.execute("""
                           CREATE TABLE "Yelp.Users" (row_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id CHAR (255), name CHAR (255), review_count INTEGER, 
                           average_stars REAL, votes CHAR (4000), friends CHAR (8000), elite REAL, yelping_since DATETIME, compliments CHAR (8000), fans INTEGER);
                           """
                           )
            self.c.commit()
        #self.count = 1
        with open (self.location_file_users) as userfile:
            for line in userfile:
                self.d = json.loads(line)
                self.values = ( ((self.row['user_id'],) if 'user_id' in self.row else (None,)) +
                    ((self.row['name'],) if 'name' in self.row else (None,))+
                    ((self.row['review_counts'],) if 'review_counts' in self.row else (None,)) +
                    ((self.row['average_stars'],) if 'average_stars' in self.row else (None,)) +
                    ((str(self.row['votes']),) if 'votes' in self.row else (None, )) +
                    ((str(self.row['friends']),) if 'friends' in self.row else (None,)) +
                    ((str(self.row['elite']),) if 'elite' in self.row else (None,)) +
                    ((self.row['yelping_since'],) if 'yelping_since' in self.row else (None,)) +
                    ((str(self.row['compliments']),) if 'compliments' in self.row else (None,)) +
                    ((self.row['fans'],) if 'fans' in self.row else (None,)) 
                        )
                self.c = self.conn.cursor()
                self.parameter_fill = ','.join('?' * len(self.values))
                self.c.execute("""
                              INSERT INTO 'Yelp.Users' (user_id, name, review_count, average_stars,
                                  votes, friends, elite, yelping_since, compliments, fans)
                                     VALUES (%s)
                              """ % self.parameter_fill, self.values)
                self.conn.commit()
        self.conn.close()
        print 'Finished.'

    def get_userdata_to_db_fastload (self):
        print 'Starting...'

        self.conn = sqlite3.connect(self.location_db)
        self.c = self.conn.cursor()
        self.c.execute ("SELECT name FROM sqlite_master WHERE type='table' AND name='Yelp.Users';")
        self.row = self.c.fetchone()
        if self.row is None:
            self.c.execute("""
                           CREATE TABLE "Yelp.Users" (row_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id CHAR (255), name CHAR (255), review_count INTEGER, average_stars REAL, votes CHAR (4000), friends CHAR (8000), elite REAL, yelping_since DATETIME, compliments CHAR (8000), fans INTEGER);
                           """
                           )
            self.c.commit()
        else:
            print "Table Yelp.Users already exists. Checking for existing user_id's."
        self.c.execute ("SELECT user_id FROM 'Yelp.Users'")
        self.existing_records = self.c.fetchall()
        self.existing_userIDs = [i[0] for i in self.existing_records]
        print "There are " + str(len(self.existing_userIDs)) + " existing user_id's"
        self.headers = ['user_id'
                        ,'name'
                        ,'review_count'
                        ,'average_stars'
                        ,'votes'
                        ,'friends'
                        ,'elite'
                        ,'yelping_since'
                        ,'compliments'
                        ,'fans']
        self.parameter_fill = ','.join('?' * len(self.headers))
        with open (self.location_file_users) as userfile:
            for i, line in enumerate(userfile):
                self.row = json.loads(line)
                self.values = ( ((self.row['user_id'],) if 'user_id' in self.row else (None,)) +
                    ((self.row['name'],) if 'name' in self.row else (None,))+
                    ((self.row['review_counts'],) if 'review_counts' in self.row else (None,)) +
                    ((self.row['average_stars'],) if 'average_stars' in self.row else (None,)) +
                    ((str(self.row['votes']),) if 'votes' in self.row else (None, )) +
                    ((str(self.row['friends']),) if 'friends' in self.row else (None,)) +
                    ((str(self.row['elite']),) if 'elite' in self.row else (None,)) +
                    ((self.row['yelping_since'],) if 'yelping_since' in self.row else (None,)) +
                    ((str(self.row['compliments']),) if 'compliments' in self.row else (None,)) +
                    ((self.row['fans'],) if 'fans' in self.row else (None,)) 
                        )

                if self.row['user_id'] in self.existing_userIDs:
                    continue
                else:
                    self.c.execute("""
                           INSERT INTO 'Yelp.Users' (user_id, name, review_count, average_stars,
                                  votes, friends, elite, yelping_since, compliments, fans)
                               VALUES (%s)
                           """ % self.parameter_fill, self.values)
                    self.conn.commit()
                    print i
        self.conn.close()
        print 'Finished.'


def main():
    y = Yelp()
    #y.get_businessdata_to_db()
    y.get_reviewdata_to_db()
    #y.get_userdata_to_db()
    #y.get_userdata_to_db_fastload()    
 
if __name__ == '__main__':
    main()
#C-u C-c C-c
