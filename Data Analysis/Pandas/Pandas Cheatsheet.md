**I will write down some codes for ones who want to better explore the data :**

**1) To get the column names of our dataframes :**

- schools.columns ,
- projects.columns,
- resources.columns ,
- donors.columns ,
- donations.columns ,
- teachers.columns

**2) To get the data type of each column of a dataframe:**

- donations.dtypes,
- schools.dtypes,
- projects.dtypes,
- resources.dtypes,
- donors.dtypes,
- teachers.dtypes,

**3) To get the number of Nan's in each column of a dataframe :**

- donations.isnull().sum(),
- schools.isnull().sum(),
- projects.isnull().sum(),
- resources.isnull().sum(),
- donors.isnull().sum(),
- teachers.isnull().sum()

**4) To understands the statistics of columns that have numeric data types.**

- donations.describe(),
- schools.describe(),
- projects.describe(),
- resources.describe(),
- donors.describe(),
- teachers.describe()

**5) To understand how many unique values that a column have :**

- schools["Name"].nunique(),
- donors["City"].nunique(),
- teachers["Teacher Prefix"].nunique()

**6) Last but not least** : if you want to change the data type of a column, lets assume that "School Percentage Free Lunch" column of schools dataframe given as string but it must be float type as expected ( actually it is ).

schools["School Percentage Free Lunch"] = schools["School Percentage Free Lunch"].astype(float)

percentiles = np.percentile(data4["Donation Amount"].dropna(), [25,75])