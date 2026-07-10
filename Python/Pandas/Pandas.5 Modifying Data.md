```python
df.columns = ["first_name","last_name","email"] #instead of first,last,email
df.columns = [x.upper() for x in df.columns]
df.columns = df.columns.str.replace(" ","_")

df.rename(columns = {"first_name": "first" , "last_name": "last"},inplace = True)

df.loc[2] = ["John", "Smith","JohnSmith@email.com"]
df.loc[2,["last","email"]] = ["Doe","JohnDoe@email.com"]
df.loc[2,"last] = "Smith"
	   
df["email"].str.lower()
df["email"] = df["email"].str.lower() #to apply to the dataframe

```
apply --> apply a function to every thing in data series
```python
df.["email"].apply(len)
def update_email(email):
	return email.upper()

df["email"].apply(update_email)
df["email"] = df["email"].apply(update_email)


df["email"] = df["email"].apply(lambda x: x.lower())

df.apply(len) #applying len function to each series returning how many rows in each column
df.apply(len,axis="columns") 
df.apply(pd.Series.min) #min value in each column in the data frame
df.apply(lambda x: x.min()) #same as the previous
```
```python
df.applymap(len) #applying to each row and column every value not a series as a whole
df.applymap(str.lower)



df["first"].map({"Corey":"Chris", "Jane":"Mary"}) #applys changes to specific values you wanted but the other values not changed take the NaN Value instead of its previous value 
```