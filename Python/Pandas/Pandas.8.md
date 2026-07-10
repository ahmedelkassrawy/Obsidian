Aggregation --> combining multiple pieces
aggregate function --> mean,mode,median
```python
df["ConvertedComp"].median()

df.describe() #display count,mean,std,min,max of the whole data frame

df["Hobbyist"].count() #gives the no. of counts only
df["Hobbyist"].value_counts() #breakdown the values and give you its count invidually
df["SocialMedia"].value_counts(normalize = True) #get it in a percentage form
```

```python
country_grp = df.groupby(["Country"]) #it will get us a new dataframe that will depend on grouping using countries only

country_grp.get_group("United States") #it displays all the info about people from united states

filt = df["Country"] == "United States"
df.loc[filt] #this is the same thing but up it will be easier with get_group to get any info about any country without having to change the filter each time


filt = df["Country"] == "United States"
df.loc[filt]["SocialMedia"].value_counts()

country_grp["SocialMedia"].value_counts() #they both do the same thing except that the country_grp shows all the stats about SocialMedia for all Countries not just United States like above

country_grp["SocialMedia"].value_counts().loc["United States"] #now this specifies it only ino US
```

```python
country_grp["ConvertedComp"].median() #gives the mean for each single country available

country_grp["ConvertedComp"].agg(["median","mean"]) #if u need two functions in the same time 
```

```python
filt = df["Country"] == "India"
df.loc[filt]["LanguageWorkedWith"].str.contains("Python").sum()
#now this uses filter to choose india as a country then filter how many of them work with python then sum them up 

country_grp["LanguageWorkedWith"].str.contains("Python").sum()
#all though its logically correct it doesnt do the same thing it approaches an Ar=ttribute Error instead

country_grp["LanguageWorkedWith"].apply(lambda x: x.str.contains("Python").sum())
#we use this insteead to do the same functionallty but here will give us the stats for whole world, For India only use loc[]
```

```python
country_respondents = df["Country"].value_counts()
country_respondents
#no. of people who are from some country 

country_uses_python = country_grp["LanguageWorkedWith"].apply(lambda x: x.str.contains("Python").sum())
country_uses_python
#apply a lambda func to do the sum up of how many user uses python

python_df = pd.concat([country_respondents,country_uses_python], axis="columns", sort=False)
#now we make a new dataframe
#use concat to put the two tables next to each other
#use axis by columns instead of rows
#let sort = False (FutureProof)

python_df.rename(columns={"count":"NumRespondents", "LanguageWorkedWith": "NumKnowsPython"},inplace = True)
#renaming for easier spelling and functinallity


python_df["PctKnowsPython"] = (python_df["NumKnowsPython"]/python_df["NumRespondents"]) * 100
#now calculating the percentage in a new column 
```