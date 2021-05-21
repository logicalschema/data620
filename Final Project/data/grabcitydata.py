# Grab 2019 data from DOB Permits
  
# import pandas module
import pandas as pd
import datetime
  
# creating a data frame
df1 = pd.read_csv("Zip_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_mon.csv")


df = df1[(df1['State'] == 'NY') & (df1['City'] == 'New York') & (df1['CountyName'] != 'Cortland County')]
print(df['RegionName'])

df.to_csv('zillow_ny.csv', index=False)