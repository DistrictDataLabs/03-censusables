import pandas as pd

################################################################################
#
# Pulls the final data set so app.py
# can load it and route it as json to an endpoint
################################################################################


df_final = pd.DataFrame.from_csv('Data/final_files/Final.csv',header = 0)
