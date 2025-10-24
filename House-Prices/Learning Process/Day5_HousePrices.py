# ====== Cell 1: Import Libraries ======
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ML-specific imports
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import cross_val_score


# ====== Cell 2: Load Dataset ======
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, 'train.csv')

if not os.path.exists(csv_path):
    raise FileNotFoundError(f"train.csv not found in {script_dir}. Make sure the file is in the same folder as this script.")

data = pd.read_csv(csv_path)
print("✅ Data loaded successfully!")
print(f"Shape: {data.shape}")

# Quick look at first few rows
print(data.head())

# ====== Cell 3: Feature Selection & Encoding ======

# Ensure full output for inspection
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# Check missing values in all columns
null_counts = data.isnull().sum()
print("Nulls per column:\n", null_counts)

# ====== Cell 3a: Handle Missing Values ======

# -----------------------------
# LotFrontage: fill missing with median by Neighborhood
# -----------------------------
data['LotFrontage'] = data.groupby('Neighborhood')['LotFrontage'].transform(
    lambda x: x.fillna(x.median())
)

# -----------------------------
# MasVnrType / MasVnrArea
# NA = no veneer / 0 area
# -----------------------------
data['MasVnrType'] = data['MasVnrType'].fillna('None')
data['MasVnrArea'] = data['MasVnrArea'].fillna(0)

# -----------------------------
# Basement-related features
# If house has no basement, fill all related vars with 'None' or 0
# -----------------------------
basement_cat = ['BsmtQual', 'BsmtCond', 'BsmtExposure', 'BsmtFinType1', 'BsmtFinType2']
for col in basement_cat:
    data[col] = data[col].fillna('None')

basement_num = ['BsmtFinSF1', 'BsmtFinSF2', 'BsmtUnfSF', 'TotalBsmtSF', 'BsmtFullBath', 'BsmtHalfBath']
for col in basement_num:
    data[col] = data[col].fillna(0)

# -----------------------------
# Garage-related features
# If house has no garage, fill categorical as 'None', numeric as 0
# -----------------------------
garage_cat = ['GarageType', 'GarageFinish', 'GarageQual', 'GarageCond']
for col in garage_cat:
    data[col] = data[col].fillna('None')

garage_num = ['GarageYrBlt']
for col in garage_num:
    data[col] = data[col].fillna(0)

# GarageCars and GarageArea are already 0 if missing? Confirm
data['GarageCars'] = data['GarageCars'].fillna(0)
data['GarageArea'] = data['GarageArea'].fillna(0)

# -----------------------------
# Electrical: fill missing with mode
# -----------------------------
data['Electrical'] = data['Electrical'].fillna(data['Electrical'].mode()[0])

# -----------------------------
# Columns with extreme missingness (Alley, PoolQC, Fence, MiscFeature)
# Fill categorical missing values with 'None'
# -----------------------------
extreme_missing_cat = ['Alley', 'PoolQC', 'Fence', 'MiscFeature', 'FireplaceQu']
for col in extreme_missing_cat:
    data[col] = data[col].fillna('None')

# Quick check
print("✅ Missing values handled. Nulls remaining per column (should be 0):\n")
print(data.isnull().sum())

# ====== Cell 4: Separate Numerical and Categorical Features ======

# Select numerical features automatically
numerical_features = data.select_dtypes(include=['int64', 'float64']).columns.tolist()

# Remove target and Id from numerical features
numerical_features = [col for col in numerical_features if col not in ['Id', 'SalePrice']]

# Select categorical features automatically
categorical_features = data.select_dtypes(include=['object']).columns.tolist()

print(f"✅ Numerical features ({len(numerical_features)}): {numerical_features[:10]} ...")
print(f"✅ Categorical features ({len(categorical_features)}): {categorical_features[:10]} ...")

# ====== Cell 4a: Inspect Categorical Consistency ======
for col in categorical_features:
    unique_vals = data[col].unique()
    print(f"{col} ({len(unique_vals)} categories): {unique_vals}")

# ====== Cell 4b: Fix Categorical Consistency ======
# MSZoning
data['MSZoning'] = data['MSZoning'].replace({'C (all)': 'C'})

# Neighborhood
data['Neighborhood'] = data['Neighborhood'].replace({'Names': 'NAmes'})

# GarageType
data['GarageType'] = data['GarageType'].replace({'Basment': 'Basement'})

# RoofStyle
data['RoofStyle'] = data['RoofStyle'].replace({'Gabrel': 'Gambrel'})

# Exterior2nd
data['Exterior2nd'] = data['Exterior2nd'].replace({'CmentBd': 'CemntBd'})

# BldgType
data['BldgType'] = data['BldgType'].replace({'Duplx': 'Duplex'})

# ====== Cell 5: Encoding Categorical Features ======
# List of categorical columns
categorical_cols = [
    'MSZoning','Street','Alley','LotShape','LandContour','Utilities','LotConfig','LandSlope',
    'Neighborhood','Condition1','Condition2','BldgType','HouseStyle','RoofStyle','RoofMatl',
    'Exterior1st','Exterior2nd','MasVnrType','ExterQual','ExterCond','Foundation','BsmtQual',
    'BsmtCond','BsmtExposure','BsmtFinType1','BsmtFinType2','Heating','HeatingQC','CentralAir',
    'Electrical','KitchenQual','Functional','FireplaceQu','GarageType','GarageFinish','GarageQual',
    'GarageCond','PavedDrive','PoolQC','Fence','MiscFeature','SaleType','SaleCondition'
]

# One-hot encode all categorical variables
data_encoded = pd.get_dummies(data, columns=categorical_cols, drop_first=True)

print("✅ Categorical variables encoded. New shape:", data_encoded.shape)

# ====== Cell 6: Model Training - Random Forest ======

# Drop 'Id' explicitly to keep only meaningful features
data_encoded = data_encoded.drop(columns=['Id'])

# Split into features and target
X = data_encoded.drop(columns=['SalePrice'])
y = data_encoded['SalePrice']

# Train-test split (80/20)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ====== Initialize Random Forest with slightly tuned parameters ======
# Hyperparameter tuning was performed using RandomizedSearchCV
# Parameters tuned: n_estimators, max_depth, min_samples_split, min_samples_leaf
# For faster execution in this portfolio, the best parameters from that search are used below
rf = RandomForestRegressor(
    n_estimators=300,   # number of trees
    max_depth=20,       # limit depth to prevent overfitting
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1           # use all cores
)

# Train the model
rf.fit(X_train, y_train)
print("✅ Random Forest trained successfully!")

# Evaluate Model
y_pred = rf.predict(X_test)

# Compute metrics
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print(f"📊 RMSE: {rmse:.2f}")
print(f"📈 R² Score: {r2:.4f}")

# ====== Feature Importance ======
importances = pd.Series(rf.feature_importances_, index=X.columns)
top_features = importances.sort_values(ascending=False).head(15)

plt.figure(figsize=(10, 6))
sns.barplot(x=top_features, y=top_features.index)
plt.title("Top 15 Feature Importances (Random Forest)")
plt.xlabel("Importance")
plt.ylabel("Feature")
plt.tight_layout()
plt.show()

# ====== Cell 7: Cross Validation ======
# Define features (X) and target (y)
X = data_encoded.drop(columns=['SalePrice'])
y = data_encoded['SalePrice']

# Initialize model
rf = RandomForestRegressor(random_state=42, n_estimators=200)

# Perform 5-fold cross validation
cv_scores = cross_val_score(rf, X, y, cv=5, scoring='neg_root_mean_squared_error')

# Convert negative RMSE to positive
rmse_scores = -cv_scores

print("Cross-validation RMSE scores:", rmse_scores)
print("Average RMSE:", rmse_scores.mean())

# Visualize cross-validation RMSE scores
plt.figure(figsize=(8, 5))
plt.plot(range(1, len(rmse_scores)+1), rmse_scores, marker='o', linestyle='--')
plt.title("Cross-Validation RMSE per Fold")
plt.xlabel("Fold Number")
plt.ylabel("RMSE")
plt.grid(True)
plt.show()

# Print summary
print(f"Average RMSE: {rmse_scores.mean():.2f}")
print(f"Standard deviation of RMSE: {rmse_scores.std():.2f}")

