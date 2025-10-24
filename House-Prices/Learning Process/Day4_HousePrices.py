"""
Day 4: House Prices Prediction (Small-Scale ML)
Author: Jake Bredice
Goal: Learn to create a machine learning model (Linear Regression), train it, evaluate results, and inspect feature importance.
"""

# ====== Cell 1: Import Libraries ======
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ML-specific imports
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# ====== Cell 2: Load the Dataset ======
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, 'train.csv')

if not os.path.exists(csv_path):
    raise FileNotFoundError(f"train.csv not found in {script_dir}. Make sure the file is in the same folder as this script.")

data = pd.read_csv(csv_path)
print("✅ Data loaded successfully!")
print(f"Shape: {data.shape}")

# ====== Cell 3: Check Important Columns & Nulls ======
columns_to_check = ['OverallQual','1stFlrSF','2ndFlrSF','TotalBsmtSF',
                    'FullBath','HalfBath','BsmtFullBath','BsmtHalfBath',
                    'YearBuilt','YearRemodAdd','YrSold','SalePrice']

print("Columns present:", columns_to_check)
print("Nulls for those columns:\n", data[columns_to_check].isnull().sum())

# ====== Cell 4: Feature Engineering ======
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

# ====== Cell 5: Train/Test Split ======
features = ['TotalSF', 'OverallQual', 'TotalBathrooms', 'HouseAge']
X = data[features]
y = data['SalePrice']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print("✅ Data split into training and test sets")
print(f"Training samples: {X_train.shape[0]}, Test samples: {X_test.shape[0]}")

# ====== Cell 6: Train Linear Regression Model ======
model = LinearRegression()
model.fit(X_train, y_train)
print("✅ Model trained successfully")

# ====== Cell 7: Make Predictions ======
y_pred = model.predict(X_test)

# ====== Cell 8: Evaluate Model Performance ======
r2 = r2_score(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
print(f"R² (goodness of fit): {r2:.2f}")
print(f"RMSE (average error in $): {rmse:.2f}")

# ====== Cell 9: Inspect Feature Influence ======
coefficients = pd.DataFrame({
    'Feature': features,
    'Coefficient': model.coef_
}).sort_values(by='Coefficient', ascending=False)

print("Feature importance (linear impact on price):")
print(coefficients)

# ====== Cell 10: Visualize Predicted vs Actual SalePrice ======
plt.figure(figsize=(8,6))
plt.scatter(y_test, y_pred, alpha=0.7)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
plt.xlabel("Actual SalePrice")
plt.ylabel("Predicted SalePrice")
plt.title("Predicted vs Actual SalePrice")
plt.show()