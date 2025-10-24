"""
Day 3: House Prices Exploration
Author: Jake Bredice
Goal: Learn basic Python, pandas, and plotting while exploring structured data.
"""

# ====== Cell 1: Import Libraries ======
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split

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

print("Shape:", data.shape)
print("Columns present:", ['OverallQual','1stFlrSF','2ndFlrSF','TotalBsmtSF',
                          'FullBath','HalfBath','BsmtFullBath','BsmtHalfBath',
                          'YearBuilt','YearRemodAdd','SalePrice'])
print("Nulls for those cols:\n", data[['OverallQual','1stFlrSF','2ndFlrSF','TotalBsmtSF',
                                       'FullBath','HalfBath','BsmtFullBath','BsmtHalfBath',
                                       'YearBuilt','YearRemodAdd','SalePrice']].isnull().sum())

# ====== Cell A: Feature engineering ======
# Create a few simple, high-impact features

# Total above-ground + basement square footage
data['TotalSF'] = data['1stFlrSF'] + data['2ndFlrSF'] + data['TotalBsmtSF']

# Total bathrooms: full + half (half counts as 0.5)
data['TotalBathrooms'] = (data['FullBath'] + 0.5 * data['HalfBath'] +
                          data['BsmtFullBath'] + 0.5 * data['BsmtHalfBath'])

# Age of house and years since remodel
data['HouseAge'] = data['YrSold'] - data['YearBuilt']        # age at sale year
data['YearsSinceRemodel'] = data['YrSold'] - data['YearRemodAdd']

# Quick glance
print(data[['TotalSF','TotalBathrooms','HouseAge','YearsSinceRemodel']].head())

corr = data[['TotalSF','TotalBathrooms','HouseAge','YearsSinceRemodel','SalePrice']].corr()
sns.heatmap(corr, annot=True, cmap='coolwarm')
plt.show()
print(data[['TotalSF','TotalBathrooms','HouseAge','YearsSinceRemodel']].isnull().sum())