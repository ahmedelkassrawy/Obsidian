```python
train_df.describe(include=["O"]) #for the categorical data

train_df.groupby(["Pclass"], as_index=False)["Survived"].mean()

family_map = {1: 'Alone', 2: 'Small', 3: 'Small', 4: 'Small', 5: 'Medium', 6: 'Medium', 7: 'Large', 8: 'Large', 11: 'Large'}

train_df['Family_Size_Grouped'] = train_df['Family_Size'].map(family_map)
```

```python
sns.displot(train_df,x="Age",col="Survived",binwidth = 10, height = 5)
#for making the chart between the Survived with = 0 and 1
```
![[Pasted image 20241016181700.png]]

```python
train_df["Age_Cut"] = pd.qcut(train_df["Age"],8) 
#cut them into 8 catgeories
```

```python
train_df.loc[train_df['Age'] <= 19, 'Age'] = 0

train_df.loc[(train_df['Age'] > 19) & (train_df['Age'] <= 25), 'Age'] = 1

train_df.loc[(train_df['Age'] > 25) & (train_df['Age'] <= 31.8), 'Age'] = 2

train_df.loc[(train_df['Age'] > 31.8) & (train_df['Age'] <= 41), 'Age'] = 3

train_df.loc[(train_df['Age'] > 41) & (train_df['Age'] <= 80), 'Age'] = 4

train_df.loc[train_df['Age'] > 80, 'Age']
```

```python
train_df['Title'] = train_df['Name'].str.split(pat= ",", expand=True)[1].str.split(pat= ".", expand=True)[0].apply(lambda x: x.strip())

#1st split the name by the comma and then takes the second part so if it was "SMith,Mr.John" --> "Mr. John"

#2nd split is the . between Mr and John we want to extract the Mr only se we select the [0] and then we strip it with the last func. of lambda

```

```python
g = sns.kdeplot(train_df['Name_Length'][(train_df['Survived']==0) & (train_df['Name_Length'].notnull())], color='Red', fill=True)

g = sns.kdeplot(train_df['Name_Length'][(train_df['Survived']==1) & (train_df['Name_Length'].notnull())], ax=g, color='Blue', fill=True)

g.set_xlabel('Name_Length')
g.set_ylabel('Frequency')
g = g.legend(['Not Survived', 'Survived'])
```

```python
train_df.groupby('TicketNumber')['TicketNumber'].transform('count')
#Takes the counts
```

## Visualization Functions

### Boxplot for Numerical Features
```python
def boxplot(data):
    num_cols = train_df.select_dtypes(exclude = 'O').columns
    for i, j in enumerate(num_cols):
        plt.subplot(len(num_cols)//3+1, 3, i+1 )
        sns.boxplot(data = data, x = j)
        plt.title(f"{j} plot")
    plt.tight_layout()

plt.figure(figsize = (15, 10))
boxplot(train_df)
```

### KDE Plot for Numerical Features
```python
def kdeplot(data):
    num_cols = train_df.select_dtypes(exclude = 'O').columns
    for i, j in enumerate(num_cols):
        plt.subplot(len(num_cols)//3+1, 3, i+1 )
        sns.kdeplot(data = data, x = j)
        plt.title(f"{j} plot")
    plt.tight_layout()

plt.figure(figsize = (15, 10))
kdeplot(train_df)
```

### Correlation Heatmap
```python
plt.figure(figsize = (15, 8))
sns.heatmap(train_df.corr(), annot = True)
plt.show()
```



