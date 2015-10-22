"""ACS5-based analysis
"""

import argparse
import json
import matplotlib.pyplot as plt
import pandas as pd

parser = argparse.ArgumentParser(__doc__)
parser.add_argument("join", help="Business/county join file")
parser.add_argument("reviews", help="Yelp review file")
parser.add_argument("census", help="ACS 5-year data")
parser.add_argument("name", help="Output name prefix")

args = parser.parse_args()

oname = args.name

# Load reviews
reviews = pd.DataFrame(json.loads(l) for l in open(args.reviews))

# Only use 2009 to 2013 reviews
reviews = reviews[reviews.date.apply(lambda d: d >= '2009' and d < '2014')]

# Reduce reviews to business review counts
reviews = (reviews[['stars']]
           .groupby(reviews.business_id)
           .count()
           .reset_index()
           )
# Fix column names
reviews.columns = 'business_id reviews'.split()

# Load the geo join data and join with the reviews
join = pd.DataFrame(json.loads(l) for l in open(args.join))
reviews = reviews.merge(join)

# Get review counts by GISJOIN
reviews = (reviews[['reviews']]
           .groupby(reviews.GISJOIN)
           .sum()
           .reset_index()
           )

# Load the 5-year census data
census = pd.read_csv(args.census)

# We want the columns that start with UEE. There should be 49.
uee = [c for c in census.columns if c.startswith('UEE')]
assert len(uee) == 49
census = census[['GISJOIN'] + uee]
# Assign more useful column names:
census.columns = '''
    GISJOIN TOTAL
    M M_4 M5_9 M10_14 M15_17 M18_19 M20 M21 M22_24 M25_29 M30_34
    M35_39 M40_44 M45_49 M50_54 M55_59 M60_61 M62_64 M65_66 M67_69
    M70_74 M75_79 M80_84 M85_
    F F_4 F5_9 F10_14 F15_17 F18_19 F20 F21 F22_24 F25_29 F30_34
    F35_39 F40_44 F45_49 F50_54 F55_59 F60_61 F62_64 F65_66 F67_69
    F70_74 F75_79 F80_84 F85_
    '''.strip().split()

# Compute young and old columns:
age_groups = {}
for n in '''
    M18_19 M20 M21 M22_24 M25_29 M30_34F18_19 F20 F21 F22_24 F25_29 F30_34
    '''.strip().split():
    age_groups[n] = 'young'
for n in '''
    M35_39 M40_44 M45_49 M50_54 M55_59 M60_61 M62_64 M65_66 M67_69
    M70_74 M75_79 M80_84 M85_
    F35_39 F40_44 F45_49 F50_54 F55_59 F60_61 F62_64 F65_66 F67_69
    F70_74 F75_79 F80_84 F85_
    '''.strip().split():
    age_groups[n] = 'old'

yo = census.groupby(age_groups, axis=1).sum()
census = pd.concat((census, yo), axis=1)

# Join with reviews
census = census.merge(reviews)

# Normalize by total population
norm = census[census.columns[3:]].div(census.TOTAL, axis=0)
census = pd.concat((census[census.columns[:3]], norm), axis=1)

# Whew, now we're ready to explore relationships. Plot response
# rate vs age-group fraction for young and old.
fig, ax = plt.subplots(2, 1)
ax[0].set_yscale('log')
ax[1].set_yscale('log')
ax[0].scatter(census.young, census.reviews, c='r', label='young')
ax[1].scatter(census.old,   census.reviews, c='b', label='old')
ax[0].set_title("ACS5 %s Yelp review rate by fraction young" % oname)
ax[1].set_title("ACS5 %s Yelp review rate by fraction old" % oname)
plt.savefig(oname+'_acs5_reviews_fraction_young_and_old.svg')

# I wonder what it would look like wo Vegas

census = census[census.GISJOIN.apply(lambda g: g[:3] != 'G32')]
fig, ax = plt.subplots(2, 1)
ax[0].set_yscale('log')
ax[1].set_yscale('log')
ax[0].scatter(census.young, census.reviews, c='r', label='young')
ax[1].scatter(census.old,   census.reviews, c='b', label='old')
ax[0].set_title("ACS5 %s Yelp review rate by fraction young no Vegas" % oname)
ax[1].set_title("ACS5 %s Yelp review rate by fraction old no Vegas" % oname)
plt.savefig(oname+'_acs5_reviews_fraction_young_and_old_no_vegas.png')
