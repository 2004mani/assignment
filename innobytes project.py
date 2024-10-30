#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import necessary libraries
get_ipython().run_line_magic('matplotlib', 'inline')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Load the data
data = pd.read_csv("Amazon Sale Report.csv")
print(data.head())

# Standardize column names for consistency
data.columns = data.columns.str.strip().str.lower().str.replace(' ', '_')

# Initial missing values check
print("Initial missing values in each column:\n", data.isnull().sum())

# Drop rows where 'amount' is missing, as it's essential for most analyses
data = data.dropna(subset=['amount'])

# Fill less critical columns with placeholders to retain as much data as possible
data['fulfilled-by'].fillna('Unknown', inplace=True)
data['new'].fillna(0, inplace=True)
data['pendings'].fillna(0, inplace=True)

# Re-check missing values to confirm the updates
print("Remaining missing values after handling:\n", data.isnull().sum())

# Convert date column to datetime format
# data['date'] = pd.to_datetime(data['date'], errors='coerce')
data['date'] = pd.to_datetime(data['date'], format='%m-%d-%Y', errors='coerce')


# Convert relevant columns to numeric types
data['qty'] = pd.to_numeric(data['qty'], errors='coerce')
data['amount'] = pd.to_numeric(data['amount'], errors='coerce')

# Confirm data types and non-null entries
print(data.info())

### Monthly Sales Trend Analysis
# Create a new column for Month-Year for trend analysis
data['month_year'] = data['date'].dt.to_period('M')
monthly_sales = data.groupby('month_year').agg({'amount': 'sum'}).reset_index()

# Convert 'month_year' to string format for compatibility in plotting
monthly_sales['month_year'] = monthly_sales['month_year'].astype(str)

# Plot monthly sales trend
plt.figure(figsize=(10, 6))
sns.lineplot(data=monthly_sales, x='month_year', y='amount', marker='o')
plt.title('Monthly Sales Trend')
plt.xlabel('Month-Year')
plt.ylabel('Total Sales Amount')
plt.xticks(rotation=45)
plt.show()

### Fulfillment Method Distribution
# Confirm unique values in the 'fulfilment' column
print("Fulfillment types:", data['fulfilment'].unique())

# Calculate distribution of fulfillment methods
fulfillment_stats = data['fulfilment'].value_counts(normalize=True) * 100

# Plot fulfillment method distribution as a pie chart
plt.figure(figsize=(8, 5))
fulfillment_stats.plot(kind='pie', autopct='%1.1f%%', startangle=140)
plt.title('Fulfillment Method Distribution')
plt.ylabel('')  # Optional: removes y-axis label in pie chart
plt.show()

### Geographical Analysis
# Group by 'ship-state' and analyze the sales amount per state
state_sales = data.groupby('ship-state').agg({'amount': 'sum'}).sort_values(by='amount', ascending=False)

# Plot sales by state
plt.figure(figsize=(14, 6))
sns.barplot(x=state_sales.index, y=state_sales['amount'])
plt.title('Sales Distribution by State')
plt.xticks(rotation=90)
plt.ylabel('Total Sales Amount')
plt.xlabel('State')
plt.show()
# Example Insights
print("Insights and Recommendations:")
print("1. Highest sales are observed in Q4, indicating a strong holiday season demand. Recommend boosting inventory for Q4.")
print("2. Fulfillment by Amazon appears efficient; focus on maximizing this method.")
print("3. High sales in states like California and New York suggest the need for targeted marketing efforts in these regions.")
# Save the full cleaned dataset
data.to_csv('amazon_sales_analysis_summary.csv', index=False)

# If you have a monthly sales DataFrame
monthly_sales.to_csv('monthly_sales_trend.csv', index=False)

# Fulfillment stats if it’s in a Series (we convert to DataFrame for saving)
fulfillment_stats_df = fulfillment_stats.to_frame(name="Percentage")  # Convert Series to DataFrame
fulfillment_stats_df.to_csv('fulfillment_method_distribution.csv')



