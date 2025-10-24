# =============================================================================
# Project: House Prices Prediction
# File: RandomForestHP.py
# Author: Jake Bredice
# Date: 2025-10-24
# Description:
#   Trains a Random Forest model to predict house prices using the Kaggle dataset.
#   Uses DataLoad.py for loading, preprocessing, and feature engineering.
#   Includes evaluation and feature importance visualization.
# =============================================================================

import os
import sys

# Add project root so we can import DataLoad
script_dir = os.path.dirname(os.path.abspath(__file__))  # Models folder
project_root = os.path.dirname(script_dir)
if project_root not in sys.path:
    sys.path.append(project_root)

import DataLoad as dl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

sns.set_style('whitegrid')

# ====== Load and preprocess data ======
train, test = dl.load_datasets()
train_encoded, test_encoded = dl.preprocess_train_test(train, test)

print(f"✅ Data ready. Train shape: {train_encoded.shape}, Test shape: {test_encoded.shape}")

# ====== Separate features and target ======
X = train_encoded.drop(columns=['SalePrice'])
y = train_encoded['SalePrice']

# Train-test split (80/20)
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# ====== Initialize Random Forest ======
rf = RandomForestRegressor(
    n_estimators=300,   # number of trees
    max_depth=20,       # limit depth to prevent overfitting
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1           # use all cores
)

# ====== Train model ======
rf.fit(X_train, y_train)
print("✅ Random Forest trained successfully!")

# ====== Evaluate model ======
y_pred = rf.predict(X_val)
rmse = np.sqrt(mean_squared_error(y_val, y_pred))
r2 = r2_score(y_val, y_pred)
print(f"📊 Validation RMSE: {rmse:.2f}")
print(f"📈 Validation R² Score: {r2:.4f}")

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

# ====== Cross-validation ======
cv_scores = cross_val_score(rf, X, y, cv=5, scoring='neg_root_mean_squared_error')
rmse_scores = -cv_scores
print("5-Fold CV RMSE scores:", rmse_scores)
print(f"Average RMSE: {rmse_scores.mean():.2f}, Std: {rmse_scores.std():.2f}")