#!~/Envs/scratch/bin/python

import requests
import json
import sqlite3

class Cluster:
    def __init__(self):
        self.api_url = 'http://clustermapping.us/data'
        self.api_year = ''
        self.api_key = ''
        self.api_payload = ''

    def get_regions(self):
        print 'Starting...'
        self.api_url_ext = '/region'
        self.r = requests.get(self.api_url + self.api_url_ext)
        self.url = self.r.url
        self.status = str(self.r.status_code)
        print self.status + ":" + self.url
        self.results = self.r.json()
        #with open ('cluster_regions.txt', 'w') as outfile:
        #    json.dump(self.results ,outfile)
        self.conn = sqlite3.connect('/home/russ/Documents/DistrictDataLabs/Censusables/Databases/Censusables.db')   
        for self.i, self.d in enumerate(self.results):
            #self.response_dict = self.results[i]
            #print self.response_dict['region_type_t']
            #print self.results['region_type_t']
            #print self.response_dict['region_code_t']
            #if self.response_dict['region_type_t'] == 'msa':
            self.keys = ( ((self.d['region_count_tl'],) if 'region_count_tl' in self.d else (None,)) +
                        ((self.d['region_short_name_t'],) if 'region_short_name_t' in self.d else (None,)) +
                        ((self.d['name_t'],) if 'name_t' in self.d else (None,)) +
                        ((self.d['region_code_t'],) if 'region_code_t' in self.d else (None,)) +
                        ((str(self.d['regions_txt']),) if 'regions_txt' in self.d else (None,)) +
                        ((str(self.d['state_codes_txt']),) if 'state_codes_txt' in self.d else (None,)) +
                        ((self.d['id'],) if 'id' in self.d else (None,)) )
            #print keys
            self.parameter_fill = ','.join('?' * 7)
            self.c = self.conn.cursor()
            self.c.execute("INSERT INTO 'Cluster.Regions' (region_count_tl, region_short_name_t, name_t, region_code_t, regions_txt, state_codes_txt, id) VALUES (%s)" % self.parameter_fill, self.keys)
            self.conn.commit()
            #print "Record:" + str(self.i)
        self.conn.close()
        print 'Finished'
        
    def get_clusterlevel_msa(self):
        print 'Starting...'
        self.api_url_ext = '/cluster/local/2013/msa/all'
        self.r = requests.get(self.api_url + self.api_url_ext)
        self.url = self.r.url
        self.status = str(self.r.status_code)
        print self.status + ":" + self.url
        self.results = self.r.json()
        #with open ('economic_data.txt', 'w') as outfile:
        #    json.dump(self.results ,outfile)
        self.conn = sqlite3.connect('/home/russ/Documents/DistrictDataLabs/Censusables/Databases/Censusables.db')
        for self.i, self.d in enumerate(self.results):
            #self.response_dict = self.results[self.i]
            #self.d = self.response_dict
            #print self.response_dict['region_type_t']
            #print self.results['region_type_t']
            #print self.response_dict
            if self.d['region_type_t'] <> '':
                #print self.d
                self.keys = ( (self.d['year_t'],) +
                        (self.d['cluster_code_t'],) +
                        ((self.d['patent_count_tf'],) if 'patent_count_tf' in self.d else (None,)) +
                        ((self.d['lq_tf_per_rank_i'],) if 'lq_tf_per_rank_i' in self.d else (None,)) +
                        (self.d['rec_count_tl'],) +
                        ((self.d['lq_tf_rank_i'],) if 'lq_tf_rank_i' in self.d else (None,)) +
                        ((self.d['emp_tl_rank_i'],) if 'emp_tl_rank_i' in self.d else (None,)) +
                        ((self.d['private_wage_tf_rank_i'],) if 'private_wage_tf_rank_i' in self.d else (None,)) +
                        (self.d['id'],) +
                        (self.d['emp_tl'],) +
                        (self.d['region_name_t'],) +
                        (self.d['region_type_t'],) +
                        (self.d['subcluster_b'],) +
                        (self.d['est_tl'],) +
                        (self.d['emp_reported_tl'],) +
                        (self.d['qp1_tl'],) +
                        (self.d['lq_tf'],) +
                        ((self.d['est_tl_rank_i'],) if 'est_tl_rank_i' in self.d else (None,)) +
                        ((self.d['emp_tl_per_rank_i'],) if 'emp_tl_per_rank_i' in self.d else (None,)) +
                        (self.d['region_short_name_t'],) +
                        (self.d['timestamp'],) +
                        ((self.d['naics_b'],) if 'naics_b' in self.d else (None,)) +
                        (self.d['key_t'],) +
                        (self.d['traded_b'],) +
                        ((self.d['est_tl_per_rank_i'],) if 'est_tl_per_rank_i' in self.d else (None,)) +
                        (self.d['region_area_type_t'],) +
                        (self.d['type_t'],) +
                        (self.d['region_emp_per_tf'],) +
                        (self.d['supression_b'],) +
                        ((self.d['private_wage_tf_per_rank_i'],) if 'private_wage_tf_per_rank_i' in self.d else (None,)) +
                        (self.d['cluster_name_t'],) +
                        (self.d['empflag_t'],) +
                        (self.d['region_code_t'],) +
                        (self.d['private_wage_tf'],) +
                        (self.d['ap_tl'],) +
                        (self.d['cluster_emp_per_tf'],) +
                        (self.d['region_key_t'],) +
                        ((self.d['sub_name_t'],) if 'sub_name_t' in self.d else (None,)) +
                        ((self.d['sub_code_t'],) if 'sub_name_t' in self.d else (None,)) +
                        ((self.d['parent_key_t'],) if 'parent_key_t' in self.d else (None,))
                        )
                self.parameter_fill = ",".join('?' * len(self.keys))
                self.c = self.conn.cursor()
                self.c.execute("INSERT INTO 'Cluster.ClusterLevel_MSA' (year_t ,cluster_code_t ,patent_count_tf ,lq_tf_per_rank_i ,rec_count_tl ,lq_tf_rank_i ,emp_tl_rank_i ,private_wage_tf_rank_i ,id ,emp_tl ,region_name_t ,region_type_t ,subcluster_b ,est_tl ,emp_reported_tl ,qp1_tl ,lq_tf ,est_tl_rank_i ,emp_tl_per_rank_i ,region_short_name_t ,timestamp ,naics_b ,key_t ,traded_b ,est_tl_per_rank_i ,region_area_type_t ,type_t ,region_emp_per_tf ,supression_b ,private_wage_tf_per_rank_i ,cluster_name_t ,empflag_t ,region_code_t ,private_wage_tf ,ap_tl ,cluster_emp_per_tf ,region_key_t ,sub_name_t ,sub_code_t ,parent_key_t) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", self.keys)
                self.conn.commit()
                print "Record:" + str(self.i)
        self.conn.close()
        print 'Finished.'

    def get_clusterlevel_msa_by_item (self):
        print 'Starting...'
        #self.msa_years = ['2013','2012','2011','2010','2009']
        #self.msa_years = ['2008','2007','2006','2005','2004','2003']
        self.msa_years = ['2002']
        self.conn = sqlite3.connect('/home/russ/Documents/DistrictDataLabs/Censusables/Databases/Censusables.db')
        for self.year in self.msa_years:
            self.c = self.conn.cursor()
            for self.msa in self.c.execute ("SELECT region_code_t FROM 'Cluster.Regions' WHERE id LIKE '%region/msa/%'"):
                self.msa_id = self.msa[0]
                self.api_url_ext = '/cluster/local/' + self.year  + '/msa/' + self.msa_id
                self.r = requests.get(self.api_url + self.api_url_ext)
                #self.url = self.r.url
                #self.status = str(self.r.status_code)
                #print self.status + ":" + self.url
                self.results = self.r.json()
                #with open ('economic_data.txt', 'w') as outfile:
                #    json.dump(self.results ,outfile)
                for self.i, self.d in enumerate(self.results):
                    #self.response_dict = self.results[self.i]
                    #self.d = self.response_dict
                    #print self.response_dict['region_type_t']
                    #print self.results['region_type_t']
                    #print self.response_dict
                    if self.d['region_type_t'] <> '':
                        #print self.d
                        self.keys = ( (self.d['year_t'],) +
                                (self.d['cluster_code_t'],) +
                                ((self.d['patent_count_tf'],) if 'patent_count_tf' in self.d else (None,)) +
                                ((self.d['lq_tf_per_rank_i'],) if 'lq_tf_per_rank_i' in self.d else (None,)) +
                                (self.d['rec_count_tl'],) +
                                ((self.d['lq_tf_rank_i'],) if 'lq_tf_rank_i' in self.d else (None,)) +
                                ((self.d['emp_tl_rank_i'],) if 'emp_tl_rank_i' in self.d else (None,)) +
                                ((self.d['private_wage_tf_rank_i'],) if 'private_wage_tf_rank_i' in self.d else (None,)) +
                                (self.d['id'],) +
                                (self.d['emp_tl'],) +
                                (self.d['region_name_t'],) +
                                (self.d['region_type_t'],) +
                                (self.d['subcluster_b'],) +
                                (self.d['est_tl'],) +
                                (self.d['emp_reported_tl'],) +
                                (self.d['qp1_tl'],) +
                                (self.d['lq_tf'],) +
                                ((self.d['est_tl_rank_i'],) if 'est_tl_rank_i' in self.d else (None,)) +
                                ((self.d['emp_tl_per_rank_i'],) if 'emp_tl_per_rank_i' in self.d else (None,)) +
                                (self.d['region_short_name_t'],) +
                                (self.d['timestamp'],) +
                                ((self.d['naics_b'],) if 'naics_b' in self.d else (None,)) +
                                (self.d['key_t'],) +
                                (self.d['traded_b'],) +
                                ((self.d['est_tl_per_rank_i'],) if 'est_tl_per_rank_i' in self.d else (None,)) +
                                (self.d['region_area_type_t'],) +
                                (self.d['type_t'],) +
                                (self.d['region_emp_per_tf'],) +
                                (self.d['supression_b'],) +
                                ((self.d['private_wage_tf_per_rank_i'],) if 'private_wage_tf_per_rank_i' in self.d else (None,)) +
                                (self.d['cluster_name_t'],) +
                                (self.d['empflag_t'],) +
                                (self.d['region_code_t'],) +
                                (self.d['private_wage_tf'],) +
                                (self.d['ap_tl'],) +
                                (self.d['cluster_emp_per_tf'],) +
                                (self.d['region_key_t'],) +
                                ((self.d['sub_name_t'],) if 'sub_name_t' in self.d else (None,)) +
                                ((self.d['sub_code_t'],) if 'sub_name_t' in self.d else (None,)) +
                                ((self.d['parent_key_t'],) if 'parent_key_t' in self.d else (None,))
                                )
                        self.c = self.conn.cursor()
                        self.parameter_fill = ','.join('?' * len(self.keys))
                        self.c.execute("INSERT INTO 'Cluster.ClusterLevel_MSA_AllYears' (year_t ,cluster_code_t ,patent_count_tf ,lq_tf_per_rank_i ,rec_count_tl ,lq_tf_rank_i ,emp_tl_rank_i ,private_wage_tf_rank_i ,id ,emp_tl ,region_name_t ,region_type_t ,subcluster_b ,est_tl ,emp_reported_tl ,qp1_tl ,lq_tf ,est_tl_rank_i ,emp_tl_per_rank_i ,region_short_name_t ,timestamp ,naics_b ,key_t ,traded_b ,est_tl_per_rank_i ,region_area_type_t ,type_t ,region_emp_per_tf ,supression_b ,private_wage_tf_per_rank_i ,cluster_name_t ,empflag_t ,region_code_t ,private_wage_tf ,ap_tl ,cluster_emp_per_tf ,region_key_t ,sub_name_t ,sub_code_t ,parent_key_t) VALUES (%s)" % self.parameter_fill, self.keys)
                        self.conn.commit()
                        print self.year +':'+ self.msa_id + ':' + str(self.i)
        self.conn.close()
        print 'Finished.'

    def get_years (self):
        print 'Starting...'
        self.api_url_ext = '/meta/years'
        self.r = requests.get(self.api_url + self.api_url_ext)
        self.url = self.r.url
        self.status = str(self.r.status_code)
        print self.status + ":" + self.url
        self.results = self.r.json()
        print self.results
       
 
if __name__ == '__main__':
    g = Cluster()
    g.get_clusterlevel_msa_by_item()
    #g.get_years()
    #print g.results

#C-u C-c C-c
