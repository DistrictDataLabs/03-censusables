from pandas import DataFrame, read_csv

import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np
import json

if __name__ == '__main__':
    print "Starting..."
    Location_Review = '/home/russ/Documents/DDL/Data/YelpData/yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_review.json' 
    reviews = pd.read_json(Location_Review, dtype={})
    

#C-u C-c C-c
