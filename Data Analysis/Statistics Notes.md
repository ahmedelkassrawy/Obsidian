## Basic Concepts

### Population and Sample
- **Population**: The entire group of interest.
- **Sample**: A subset of the population used for analysis.

### Types of Data

#### Qualitative Data
- **Nominal**: Categories without order, e.g., male/female, green/red/blue.
- **Ordinal**: Categories with order, e.g., poor, fair, good, excellent.

#### Quantitative Data
- **Discrete**: Countable values.
- **Continuous**: Values within a range.

## Applications of Statistics
- Fraud Detection
- Recommendation Systems
- Analytics

## Descriptive Statistics
Provides a clear understanding of data through numerical calculations.

### Data Organization
- **Cases**: Rows in a dataset.
- **Variables**: Columns in a dataset.
- **Data Matrix**: A structure to keep all details of each individual case.
- **Frequency Table**: A summary showing how often each value of a variable occurs. Useful for quickly grasping data distribution across categories or ranges.

## Measures of Central Tendency
- **Mean**: Average value.
- **Median**: Middle value when data is ordered.
- **Mode**: Most frequent value.

## Measures of Dispersion
Describes the spread or variability in the data.
- **Range**: Difference between maximum and minimum values.
- **Variance**: Average squared deviation from the mean.
- **Standard Deviation**: Square root of variance; measures average distance from the mean.
- **IQR (Interquartile Range)**: Q3 - Q1, used to identify outliers.
  - To calculate: Arrange data in ascending order, find Q1 (25th percentile) and Q3 (75th percentile).
  - Outliers: Values below Q1 - 1.5 * IQR or above Q3 + 1.5 * IQR.

## Data Visualization
- **Histogram**: Organizes data to identify patterns.
- **Box Plot**: Identifies outliers and shows data distribution.

## Central Limit Theorem (CLT)
The CLT states that the sampling distribution of the sample mean will be approximately normally distributed, regardless of the population's distribution, for large sample sizes.

## Hypothesis Testing
- **H0 (Null Hypothesis)**: The default assumption (no effect or no difference).
- **H1 (Alternative Hypothesis)**: The claim to test (there is an effect or difference).
- **P-value**: Probability of observing the sample data assuming H0 is true.
- **Significance Level (α)**: Threshold chosen before the test (commonly 0.05).

### Steps in Hypothesis Testing
1. State the Hypotheses: Define H0 and H1.
2. Select a Significance Level (α): Commonly set at 0.05.
3. Collect Data and Calculate a Test Statistic: e.g., t-statistic or z-statistic.
4. Find the P-value: Compare the test statistic to the theoretical distribution.
5. Make a Decision:
   - If p-value < α, reject H0 (evidence suggests an effect).
   - If p-value ≥ α, do not reject H0 (insufficient evidence).

## Linear Algebra Concepts
- **Eigenvalue (λ)**: A scalar indicating how much the eigenvector is stretched or compressed.
- **Eigenvector (v)**: A vector that does not change its direction during the transformation.