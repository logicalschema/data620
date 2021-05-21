# Look at zillow data 

# import pandas module
import pandas as pd
import datetime

# creating a data frame
df = pd.read_csv("zillow_ny.csv")



print(df['CountyName'].unique())