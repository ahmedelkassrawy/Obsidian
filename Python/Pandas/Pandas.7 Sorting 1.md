```python
import pandas as pd

df.sort_values(by="last")

df.sort_values(by="last",ascending=False)

df.sort_values(by=["last","first"],ascending=False) #at duplicates at last name the sorting will then go to the first name option to sort upon it

df.sort_values(by=["last","first"],ascending=[False,True]) #same as what happend above but at the ascending option for the last name it will be False but at first it will become True

df["last"].sort_values() #sorting the last names values in ascending order

df.sort_index() #sorting according to the index
```

```python
df.sort_values(by=["Country","SalaryUSD"],ascending=[True,False],inplace=True) #sorting using Country and salary and inplacing it to the original data frame

df[["Country","SalaryUSD"]].head(50) #displaying the first 50 salary and country together

df["SalaryUSD"].nlargest(10) #shows the highest 10 Salarys in the column of Salary only appears no further info

df.nlargest(10,"SalaryUSD") #returns all info about the people with highest 10 
```