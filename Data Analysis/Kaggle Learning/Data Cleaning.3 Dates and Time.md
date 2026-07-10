```python
import pandas as pd
import numpy as np
import datetime

#import data bta3tk
#dates 4klha 3/2/07
```
`%d` for day, `%m` for month, `%y` for a two-digit year and `%Y` for a four digit year.
- 1/17/07 has the format "%m/%d/%y"
- 17-1-2007 has the format "%d-%m-%Y"
```python
# create a new column, date_parsed, with the parsed dates
landslides['date_parsed'] = 
pd.to_datetime(landslides['date'], format="%m/%d/%y")

# get the day of the month from the date_parsed column
day_of_month_landslides = landslides['date_parsed'].dt.day
day_of_month_landslides.head()
```