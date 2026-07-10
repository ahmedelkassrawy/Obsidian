```python
import pandas as pd
from datetime import datetime

df["Data"] = pd.to_datetime(df["Date"]) #to identify timestamps correctly
df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d %I-%p") #this format is from the pandas docs

df.loc[0,"Date"].day_name() #returns the name of the day

df["Date"].dt.day_name()  #to return names of the day for the whole dataframe

df["Date"].min() #return the first date in dataframe
df["Date"].max() #return the last date in dataframe

df["Date"].max() - df["Date"].min() #time delta between the two dates

filt = (df["Date"] >= "2020")
df.loc[filt] #to get all the dates in 2020

filt = (df["Date"] >= "2019") & (df["Date"] < "2020")
df.loc[filt] #get all days from 2019 and before 2020

df.set_index("Date",inplace = True)
df["2019"]
df["2020-01":"2020-02"] #slicing works

df["High"].resample("D").max() #giving the High column values in days not in hourly stamps using resampling

highs = df["High"].resample("D").max()
highs["2020-01-01"]

%matplotlib inline #for creatin plots in jupyter notebooks
highs.plot() 

df.resample("W").agg({"Close": "mean","High":"max","Low":"min","Volume":"sum"}) #using resampling and the agg functions all together
```