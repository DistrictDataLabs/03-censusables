#!~/anaconda/bin/ python


###############################################################################
# 
# This uses PCA analysis tools to save the Final.csv file which
# will be used to rank zip codes according to the 4 parameters (income,
# housing, diversity, and population density
#
#
###############################################################################

################################################################################
# Imports
################################################################################

import pandas as pd
import numpy as np
from sklearn.decomposition import PCA as sklearnPCA
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler

################################################################################
# File Paths
################################################################################

#File locations
acs_file = "../Data/raw_files/acs5yr.csv"
zillow_HVI_file = "../Data/raw_files/Zip_Zhvi_AllHomes_HomeValueIndex.csv"
zillow_RI_file = "../Data/raw_files/Zip_Zri_AllHomes_RentIndex.csv"
urbanization_zip = "../Data/raw_files/zcta2010_txt.csv"
ZCTA = "../Data/raw_files/ZCTA.csv"
Final = "../Data/final_files/Final.csv"

################################################################################
# Function Definitions
################################################################################

def pca_analysis(indexname,dataframe):
    df = dataframe
    column_count = len(df.columns)

    X = df.ix[:,1:column_count].values
    zip = df.ix[:,0].values

    #Standardize Data
    X_std = StandardScaler().fit_transform(X)
        
    #Generate PCA Components
    sklearn_pca = sklearnPCA(n_components=1)
    Y_sklearn = sklearn_pca.fit_transform(X_std)

    explained_ratio = sklearn_pca.explained_variance_ratio_
    covariance_array = sklearn_pca.get_covariance()

    df_final = pd.DataFrame({'zip5':zip,indexname:Y_sklearn[:,0]})
    
    #Normalize Data on a 0 to 1 scale
    zip5_final = df_final['zip5'].values
    minmax_scale = preprocessing.MinMaxScaler().fit(df_final[[indexname]])
    minmax = minmax_scale.transform(df_final[[indexname]])
    df_minmax = pd.DataFrame({'zip5':zip5_final,indexname:minmax[:,0]})

    return df_minmax    

################################################################################
# Main Execution
################################################################################
def main():
    #ACS DATA (Diversity, Income, and Population Density)
    acs = pd.read_csv(acs_file)

    #Generate Diversity Index from race fields
    diversity = acs[['zip5','pop','race_white','race_black','race_asian','race_indian','race_other','hisp']].copy(deep=True)
    diversity['white_hisp'] = ((diversity['pop']*diversity['race_white'])*diversity['hisp'])/diversity['pop']
    diversity['white_nonhisp'] = ((diversity['pop']*diversity['race_white'])*(1-diversity['hisp']))/diversity['pop']
    diversity['div_index'] = 1- (diversity['race_black']**2 + diversity['white_hisp']**2 + diversity['white_nonhisp']**2 + diversity['race_asian']**2 + diversity['race_indian']**2)
    diversity_index = diversity[['zip5','div_index']].dropna(axis=0,how='any',subset=['zip5','div_index'])

    #Generate Income Index
    income_index = acs[['zip5','inc_median','poverty','snap','gini_index']].dropna(axis=0,how='all')

    #Population Density
    urban = pd.read_csv(urbanization_zip)
    urban.rename(columns={'Zip5':'zip5'},inplace=True)
    urban['zip5'] = urban.apply(lambda x: int(x['zip5']),axis=1)
    urban['pop'] = urban.apply(lambda x: int(x['POPULATION']),axis=1)
    urban['urban_index'] = urban['pop']/urban['LANDSQMT']
    #print urban[urban.isnull().any(axis=1)]
    #urban_index = urban[['zip5','urban_index']][urban['pop']>0]
    urban_index = urban[['zip5','urban_index']].dropna(axis=0,how='any',subset=['zip5','urban_index'])

    
    #Zillow Data (Housing Cost)
    zillow_HVI = pd.read_csv(zillow_HVI_file)
    zillow_RI = pd.read_csv(zillow_RI_file)

    
    zillow_HVI = zillow_HVI[['RegionName','2014-01','2014-07','2015-01','2015-07']]
    zillow_HVI.rename(columns={'RegionName':'zip5'},inplace=True)

    zillow_RI = zillow_RI[['RegionName','2014-01','2014-07','2015-01','2015-07']].copy(False)
    zillow_RI.rename(columns={'RegionName':'zip5'},inplace=True)
    housing_index = pd.merge (zillow_HVI, zillow_RI,how='inner', on='zip5').dropna(axis=0,how='all')
    housing_index.loc[housing_index['2014-07_x'].isnull(),'2014-07_x'] = housing_index['2014-01_x']

    #Return Normalized PCA Dataframes
    df_inc = pca_analysis('income_index',income_index)    
    df_hou = pca_analysis('housing_index',housing_index)    
    #Reverse Housing Index so higher cost = higher index 
    df_hou['housing_index']= df_hou.apply(lambda x: 1-x['housing_index'],axis=1)    
    df_div = pca_analysis('diversity_index',diversity_index)    
    df_urb = pca_analysis('urban_index',urban_index)

    #Combine DataFrames from each separate index
    df = pd.merge (df_inc,df_hou,on='zip5')
    df = pd.merge (df,df_urb,on='zip5')
    df = pd.merge (df,df_div,on='zip5')
    
    #Add Zip Code Descriptions
    ZipCode = pd.read_csv(ZCTA)
    df_all_final = pd.merge (df,ZipCode[['zcta5','ZIPName','State']],left_on='zip5',right_on='zcta5',copy=False)
    del df_all_final['zcta5']
    df_all_final = pd.merge(df_all_final,urban[['zip5','ZCTA5']],copy=False)

    #Write DataFrame to File
    df_all_final.to_csv(Final)
    
    
if __name__ == '__main__':
    main()
