1. look at the unique values in a column 
2. if there is inconsistency try making it lower case for all or upper case for all. 
**Fuzzy matching:** The process of automatically finding text strings that are very similar to the target string.

So "apple" and "snapple" are two changes away from each other (add "s" and "n") while "in" and "on" and one change away (rplace "i" with "o"). You won't always be able to rely on fuzzy matching 100%, but it will usually end up saving you at least a little time.

```python
matches = fuzzywuzzy.process.extract("south korea",countries, limit = 10, scorer=fuzzywuzzy.fuzz.token_sort_ratio)

matches
#[('south korea', 100),
 #('southkorea', 48),
# ('saudi arabia', 43),
# ('norway', 35),
# ('austria', 33),
# ('ireland', 33),
# ('pakistan', 32),
# ('portugal', 32),
# ('scotland', 32),
 #('australia', 30)]
```

```python
# function to replace rows in the provided column of the provided dataframe
# that match the provided string above the provided ratio with the provided string
def replace_matches_in_column(df, column, string_to_match, min_ratio = 47):
    # get a list of unique strings
    strings = df[column].unique()
    
    # get the top 10 closest matches to our input string
    matches = fuzzywuzzy.process.extract(string_to_match, strings, limit=10, scorer=fuzzywuzzy.fuzz.token_sort_ratio)

# only get matches with a ratio > 90
    close_matches = [matches[0] for matches in matches if matches[1] >= min_ratio]

    # get the rows of all the close matches in our dataframe
    rows_with_matches = df[column].isin(close_matches)
    
# replace all rows with close matches with the input matches 
    df.loc[rows_with_matches, column] = string_to_match
    
    # let us know the function's done
    print("All done!")
```
