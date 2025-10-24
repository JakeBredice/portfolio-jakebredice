"""
Day 2: House Prices Exploration
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
print("✅ Data loaded successfully!")
print(f"Shape: {data.shape}")

# ====== Cell 2: Handle Missing Values ======
print("\nMissing values before cleaning:")
print(data.isnull().sum().sort_values(ascending=False).head(10))

# Drop columns that are almost entirely empty
data = data.drop(columns=['PoolQC'])  # Too few non-null values to be useful

# Fill numeric nulls
data['LotFrontage'] = data['LotFrontage'].fillna(data['LotFrontage'].median())
data['MasVnrArea'] = data['MasVnrArea'].fillna(0)
data['GarageYrBlt'] = data['GarageYrBlt'].fillna(data['GarageYrBlt'].median())

# Fill categorical nulls
data['Electrical'] = data['Electrical'].fillna(data['Electrical'].mode()[0])
data['GarageType'] = data['GarageType'].fillna('None')

# Handle categorical columns with meaningful missing values
data['Alley'] = data['Alley'].fillna('NoAlley')
data['Fence'] = data['Fence'].fillna('NoFence')
data['MiscFeature'] = data['MiscFeature'].fillna('None')
data['MasVnrType'] = data['MasVnrType'].fillna('None')
data['FireplaceQu'] = data['FireplaceQu'].fillna('NoFireplace')
data['GarageQual'] = data['GarageQual'].fillna('NoGarage')
data['GarageFinish'] = data['GarageFinish'].fillna('NoGarage')
data['GarageCond'] = data['GarageCond'].fillna('NoGarage')
data['BsmtExposure'] = data['BsmtExposure'].fillna('NoBsmt')
data['BsmtFinType1'] = data['BsmtFinType1'].fillna('NoBsmt')
data['BsmtFinType2'] = data['BsmtFinType2'].fillna('NoBsmt')
data['BsmtCond'] = data['BsmtCond'].fillna('NoBsmt')
data['BsmtQual'] = data['BsmtQual'].fillna('NoBsmt')

print("\n✅ Missing values handled.")
print(f"Remaining missing values: {data.isnull().sum().sum()}")

print("\nMissing values after cleaning:")
print(data.isnull().sum().sort_values(ascending=False).head(10))

# ====== Cell 3: Histogram of SalePrice ======
plt.figure(figsize=(8,5))
plt.hist(data['SalePrice'], bins=30, color='skyblue', edgecolor='black')
plt.title('Distribution of House Prices')
plt.xlabel('SalePrice')
plt.ylabel('Number of Houses')
plt.show()

# ====== Cell 4: Select Numeric Features for Quick Exploration ======
# For now, focus on numeric features to simplify learning
numeric_features = data.select_dtypes(include=[np.number])
print("Numeric features:")
print(numeric_features.columns.tolist())

# Check correlations with SalePrice
corr_with_target = numeric_features.corr()['SalePrice'].sort_values(ascending=False)
print("\nTop features correlated with SalePrice:")
print(corr_with_target.head(10))

# ====== Cell 5: Encode Categorical Features (Simple Learning Version) ======
# Convert categorical features into dummy variables for regression
categorical_features = data.select_dtypes(include=[object])
print("Categorical features (sample):")
print(categorical_features.columns[:10])

# Example: convert a few key features for learning
encoded_data = pd.get_dummies(data, columns=['MSZoning', 'Street', 'LotShape'], drop_first=True)

print("\nColumns after encoding:")
print(encoded_data.columns[:20])

# ====== Cell 6: Visualize Top Numeric Feature vs SalePrice ======
# From correlation analysis, OverallQual is highly correlated with SalePrice
plt.figure(figsize=(8,5))
plt.scatter(data['OverallQual'], data['SalePrice'], color='orange')
plt.title('SalePrice vs Overall Quality')
plt.xlabel('Overall Quality')
plt.ylabel('SalePrice')
plt.show()