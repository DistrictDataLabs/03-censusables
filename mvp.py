"""MVP (Really week 1 progress)

This script assumes that geo joins have already been done by the
geojoin script and that there is a business/county join that's passed
in on the command line.

"""

import argparse
import json
import matplotlib.pyplot as plt
import pandas as pd

parser = argparse.ArgumentParser(__doc__)
parser.add_argument("join", help="Business/county join file")
parser.add_argument("businesses", help="Yelp business file")
parser.add_argument("reviews", help="Yelp review file")
parser.add_argument("census2010", help="ACS1 county estimates for 2010")
parser.add_argument("census2011", help="ACS1 county estimates for 2010")
parser.add_argument("census2012", help="ACS1 county estimates for 2010")
parser.add_argument("census2013", help="ACS1 county estimates for 2010")

args = parser.parse_args()

# Load reviews
reviews = pd.DataFrame(json.loads(l) for l in open(args.reviews))
reviews['YEAR'] = reviews.date.str.slice(0, 4).astype('int64')

# Show review counts by year:
reviews_by_year = reviews.YEAR.value_counts()
plt.figure().add_subplot(1,1,1)
reviews_by_year.plot(kind='bar').set_title('Yelp review counts by year.')
plt.savefig('reviews_by_year.svg')

# Reduce reviews to business-year review counts
reviews = (reviews[['stars']]
           .groupby([reviews.business_id, reviews.YEAR])
           .count()
           .reset_index()
           )
# Fix column names
reviews.columns = 'business_id YEAR reviews'.split()

# Load the geo join data and join with the reviews
join = pd.DataFrame(json.loads(l) for l in open(args.join))
reviews = reviews.merge(join)

# Get review counts by GISJOIN and year
reviews = (reviews[['reviews']]
           .groupby([reviews.GISJOIN, reviews.YEAR])
           .sum()
           .reset_index()
           )

# Load the one-year census data
census = (pd.read_csv(args.census2010),
          pd.read_csv(args.census2011),
          pd.read_csv(args.census2012),
          pd.read_csv(args.census2013),
          )

# Select the columns we want and concat.  This is awkward, because
# 1) column names for demographic data are different across years, and
# 2) when I downloaded 2013, i didn't ask for unweighted totals.  This is
# an easy mistake to make. But I know I want GISJOIN, YEAR and the last 49
# columns, so...
census = [c[['GISJOIN', 'YEAR'] + list(c.columns[-49:])] for c in census]

# Assign more useful column names:
for c in census:
    c.columns = '''
    GISJOIN YEAR TOTAL
    M M_4 M5_9 M10_14 M15_17 M18_19 M20 M21 M22_24 M25_29 M30_34
    M35_39 M40_44 M45_49 M50_54 M55_59 M60_61 M62_64 M65_66 M67_69
    M70_74 M75_79 M80_84 M85_
    F F_4 F5_9 F10_14 F15_17 F18_19 F20 F21 F22_24 F25_29 F30_34
    F35_39 F40_44 F45_49 F50_54 F55_59 F60_61 F62_64 F65_66 F67_69
    F70_74 F75_79 F80_84 F85_
    '''.strip().split()

# Combine
census = pd.concat(census, ignore_index=True)

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
ax = plt.figure().add_subplot(1,1,1)
plt.scatter(census.young, census.reviews, c='r', label='young')
plt.scatter(census.old,   census.reviews, c='b', label='old')
ax.set_title("Yelp review rate by fraction young and old for multiple years")
ax.legend()
plt.savefig('reviews_fraction_young_and_old_multiyear.svg')

# Well, no obvious pattern there. Perhaps it would be clearer if we
# aggregate by year.
census4 = (census[census.columns[1:]]
           .groupby(census.GISJOIN)
           .mean()
           )
ax = plt.figure().add_subplot(1,1,1)
plt.scatter(census4.young, census4.reviews, c='r', label='young')
plt.scatter(census4.old,   census4.reviews, c='b', label='old')
ax.set_title("Yelp review rate by fraction young and old mean over 4 years")
ax.legend()
plt.savefig('reviews_fraction_young_and_old_mean.svg')

# Nope, wtf that weird peak in the middle.  There must be some other
# effect.  We only have 15 counties.  Let's see how reviews are
# distributed among them:
ax = plt.figure().add_subplot(1,1,1)
census4.reviews.plot(kind='bar')
ax.set_title("Reviews by county")
plt.subplots_adjust(bottom=.2)
plt.savefig('reviews_by_county.svg')

# The reviews are dominated by a single county, which is Clark County,
# NV, which includes Las Vegas.  Hm.  Yelp reviews are probably
# concentrated in just the sort of businesses that are prominent in
# Las Vegas.  Let's look at yelp reviews by category. The category is
# in an array value.
cats = []
for d in (json.loads(l) for l in open(args.businesses)):
    for c in d['categories']:
        cats.append(dict(business_id = d['business_id'], category=c))
cats = pd.DataFrame(cats)
cats = cats.category.value_counts()
cats.name = 'reviews'
ax = plt.figure().add_subplot(1,1,1)
cats[:30].plot(kind='bar')
ax.set_title("Reviews by category")
plt.subplots_adjust(bottom=.4)
plt.savefig('reviews_by_category.svg')

# Yup, the most popular yelp categories are those that are likely to
# be pretty important in Las Vegas.

# This data isn't really telling us very much.  We need to think about
# the Las Vegas issue. It's likely that yelp activity is qualitatively
# different there. Perhaps there's a way to test that.

# We probably need to go to ACS 5-year data so we could get more
# geographic diversity.  We feared that demographics would change too
# much over the 5 year period. We can test that by looking at the
# ratio of standard deviation to mean over time for out demographic data.

def std_by_mean(a):
    return a.std() / a.mean()

var = (census[census.columns[3:-1]]
       .groupby(census.GISJOIN)
       .agg(std_by_mean)
       .describe()
       .stack()
       .unstack(0)
       )
var['max'] = var['max'] - var['75%']
var['75%'] = var['75%'] - var['50%']
var['50%'] = var['50%'] - var['25%']
var['25%'] = var['25%'] - var['min']
ax = plt.figure().add_subplot(1,1,1)
ax.set_title("Distribution of std/mean of fraction of demo groups")
var[['min', '25%', '50%', '75%', 'max']].plot(kind='bar', stacked=True)
ax.legend()
plt.subplots_adjust(bottom=.2)
plt.savefig('variability.svg')

# The variability is generally pretty low, although it's high for some
# demographic county combinations. Then again, some of the demographic
# categories are pretty small and thus subject to lots of variation.
# The variability in larger categories (e.g. young and old) is pretty
# small.
