Line Plot
```python
x = [1,2,3,4,5]
y = [2,3,5,7,11]

plt.plot(x,y)
plt.title("Simple Line Plot")
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.show()
```

![[Pasted image 20260129210542.png]]
Scatter Plot
```python
import matplotlib.pyplot as plt

# Data points
x = [5, 7, 8, 7, 2, 17, 2, 9]
y = [99, 86, 87, 88, 100, 86, 103, 87]

# Create plot
plt.scatter(x, y)
plt.title("Simple Scatter Plot")
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.show()
```

![[Pasted image 20260129210706.png]]

Bar Chart
```python
categories = ['A', 'B', 'C', 'D']
values = [4, 7, 1, 8]

plt.bar(categories, values, color='blue')
plt.title("Simple Bar Chart")
plt.xlabel("Categories")
plt.ylabel("Values")
plt.show()
```

Create a bar chart with specified categories and their corresponding values
![[Pasted image 20260129210847.png]]

Histogram
```python
data = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5]

plt.hist(data, bins=5, color='green')

plt.title("Simple Histogram")
plt.xlabel("Bins")
plt.ylabel("Frequency")
plt.show()
```
- A histogram is used to show the distribution of a numerical variable.
- histogram with a specified number of bins
![[Pasted image 20260129211021.png]]

| **Feature**   | **Bar Chart**                               | **Histogram**                                    |
| ------------- | ------------------------------------------- | ------------------------------------------------ |
| **Data Type** | **Categorical** (Labels like 'A', 'B', 'C') | **Numerical** (Numbers like 1, 2, 3)             |
| **Purpose**   | Compares values across different categories | Shows the distribution/frequency of data         |
| **Spacing**   | Usually has gaps between bars               | Bars are typically touching (to show continuity) |
| **Example**   | Sales per Department                        | Distribution of employee ages                    |

Subplots
```python
x = [1, 2, 3, 4, 5]

y1 = [1, 4, 9, 16, 25]
y2 = [1, 2, 3, 4, 5]

plt.subplot(1, 2, 1)
plt.plot(x, y1, 'r-')
plt.title("Plot 1")

plt.subplot(1, 2, 2)
plt.plot(x, y2, 'g-')
plt.title("Plot 2")

plt.show()
```
- plt.subplot(nrows,ncols,index)
![[Pasted image 20260129211249.png]]

**Outliers (Anomalies)**
- Technical Bug
- Data Entry Error
- Extreme Case

**Identify Outliers**
- Box Plots 
- Scatter Plot
- Histogram
- Density Plot 

Density Plot: Provides a smooth curve of the data distribution, with outliers showing up as irregular bumps outside the main peak

---
#### Seaborn
- **Visualizing Distributions**: Histograms, KDE plots, and rug plots. 
- **Visualizing Categorical** Data: Bar plots, count plots, box plots, and violin plots.
- **Visualizing Relationships**: Scatter plots, line plots, and pair plots. 
- **Heatmaps**: For showing data correlations.

Line Plot
```python
import seaborn as sns
import matplotlib.pyplot as plt

data = sns.load_dataset("tips")
sns.lineplot(x="total_bill", y="tip", data=data)
plt.title("Line Plot with Seaborn")
plt.show()
```
![[Pasted image 20260129211658.png]]

Regression Line
```python
sns.lmplot(x='total_bill', y='tip', data=data)
plt.title("Scatter Plot with Regression Line")
plt.show()
```
![[Pasted image 20260129211824.png]]

Bar Chart
```python
sns.barplot(x='day', y='total_bill', data=data)
plt.title("Bar Plot")
plt.show()
```
- showing the average total bill for each day of the week
![[Pasted image 20260129211923.png]]

Box Plot
```python
sns.boxplot(x='day', y='total_bill', data=data)
plt.title("Box Plot")
plt.show()
```
- highlighting the median, quartiles, and potential outliers
![[Pasted image 20260129212016.png]]

Heatmap 
```python
# Load a dataset using Seaborn
data = sns.load_dataset('tips')

# Select only the numerical columns
numerical_data = data.select_dtypes(include=['float64', 'int64'])

# Compute the correlation matrix
corr = numerical_data.corr()

# Plot the heatmap
sns.heatmap(corr, annot=True, cmap='coolwarm')
plt.title("Heatmap of Correlation Matrix")
plt.show()
```
- ) visualizes the correlation matrix
![[Pasted image 20260129212119.png]]

Line Plot -> to show trends over time
Scatter plot -> Visualize relationships between 2 variables
Bar plot -> Categorical Data
Histogram -> data distribution 
	The KDE (Kernel Density Estimate) line provides a smoothed version of the distribution, making it easier to see the underlying pattern
Box plot -> Visualize Distribution and Outliers
Violin Plot -> Show Density and Distribution
	Violin plots combine the features of box plots and KDE
```python
sns.violinplot(x='day', y='total_bill', data=data)

plt.title("Total Bill Distribution by Day (Violin Plot)")
plt.xlabel("Day")
plt.ylabel("Total Bill")
plt.show()
```
![[Pasted image 20260129212616.png]]

Pair Plot ->  Show Pairwise Relationships
```python
sns.pairplot(data)
plt.suptitle("Pairwise Relationships in the Tips Dataset", y=1.02)
plt.show()
```
![[Pasted image 20260129212720.png]]

Count Plot -> Show the Frequency of Categorical Values
Count plots visualize the frequency of occurrences for categorical data.
```python
sns.countplot(x='day', data=data)
plt.title("Count of Tips by Day")
plt.show()
```
![[Pasted image 20260129212813.png]]

Joint Plot to Show Distribution and Relationship
combines a scatter plot and histograms
```python
sns.jointplot(x='total_bill', y='tip', data=data, kind='scatter') plt.suptitle("Joint Distribution of Total Bill and Tip", y=1.02) plt.show()
```
![[Pasted image 20260129212927.png]]

Outliers
```python
for col in df.columns:
    # 1. Visualization Before
    sns.boxplot(x=df[col])
    plt.title(f"Before: {col}")
    plt.show()

    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    df[col] = df[col].clip(lower=lower_bound, upper=upper_bound)

    # 4. Visualization After
    sns.boxplot(x=df[col])
    plt.title(f"After: {col}")
    plt.show()

    print("="*30)
```

Heatmap
```python
corr = df.corr()

sns.heatmap(data = corr , annot = True, cmap = "coolwarm")
plt.show()
```

Map
```python
# The intersection of Latitude and Longitude would essentially draw a "map" of where the housing blocks are located in California.
sns.scatterplot(x="Longitude", y="Latitude", data=df)
```

Hack for pairplot
```python
# Sample the data
sns.pairplot(df.sample(1000))

# Select specific columns
sns.pairplot(df.sample(100)[['MedInc', 'HouseAge', 'AveRooms', 'MedHouseVal']])
```

Regression plot
```python
plt.figure(figsize=(10, 6))
sns.regplot(data=df, x='MedInc', y='MedHouseVal',
            scatter_kws={'alpha':0.3, 's':10}, # Make dots transparent and small
            line_kws={'color':'red'})          # Make the trend line red

# 3. Add labels and title
plt.title('Relationship Between Income and House Value')
plt.xlabel('Median Income (Tens of Thousands $)')
plt.ylabel('Median House Value (Hundreds of Thousands $)')

plt.show()
```