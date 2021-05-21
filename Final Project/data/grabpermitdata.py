# Grab 2019 data from DOB Permits
  
# import pandas module
import pandas as pd
import datetime
  
# creating a data frame
df = pd.read_csv("DOB_NOW__Build___Approved_Permits.csv")
print(df.head())

df['Issued Date'] = pd.to_datetime(df['Issued Date'])
df['Approved Date'] = pd.to_datetime(df['Approved Date'])
df['Expired Date'] = pd.to_datetime(df['Expired Date'])

# Typical format for Issued data
# 2016 Jun 23 08:15:04 AM 
#print(df['Issued Date'])
print(df.dtypes)

print(df['Issued Date'].head())
print(df['Approved Date'].head())
print(df['Expired Date'].head())

df_2019 = df[df['Issued Date'].dt.year == 2019]

print(df_2019['Issued Date'].head())


df_2019.to_csv('dob_issue_2019_permits.csv', index=False)



