"""
Day 1: House Prices Exploration
Author: Jake Bredice
Goal: Learn basic Python, pandas, and plotting while exploring structured data.
"""

# ====== Cell 1: Import Libraries ======
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ====== Cell 2: Load the Dataset ======
# Automatically find 'train.csv' in the same folder as this script
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, 'train.csv')

# Check if the file exists
if not os.path.exists(csv_path):
    raise FileNotFoundError(f"train.csv not found in {script_dir}. Make sure the file is in the same folder as this script.")

data = pd.read_csv(csv_path)
print("First 5 rows of the dataset:")
print(data.head())

# ====== Cell 3: Dataset Info ======
print("\nDataset Info:")
print(data.info())

# ====== Cell 4: Summary Statistics ======
print("\nSummary Statistics:")
print(data.describe())

# ====== Cell 5: Check Missing Values ======
print("\nMissing Values:")
print(data.isnull().sum())

# ====== Cell 6: Histogram of SalePrice ======
import matplotlib.pyplot as plt
plt.figure(figsize=(8,5))
plt.hist(data['SalePrice'], bins=30, color='skyblue', edgecolor='black')
plt.title('Distribution of House Prices')
plt.xlabel('SalePrice')
plt.ylabel('Number of Houses')
plt.show()

# ====== Cell 7: Scatter Plot – Overall Quality vs SalePrice ======
plt.figure(figsize=(8,5))
plt.scatter(data['OverallQual'], data['SalePrice'], color='orange')
plt.title('Sale Price vs. Overall Quality')
plt.xlabel('Overall Quality')
plt.ylabel('Sale Price')
plt.show()

# ====== Cell 8: Correlation Heatmap ======
plt.figure(figsize=(12,8))
numeric_features = data.select_dtypes(include=[np.number])
corr = numeric_features.corr()

# show only strong correlations for readability
sns.heatmap(corr[['SalePrice']].sort_values(by='SalePrice', ascending=False), 
            cmap='coolwarm', annot=True, fmt=".2f")
plt.title('Correlation of Numeric Features with Sale Price')
plt.show()