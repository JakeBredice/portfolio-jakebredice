# =============================================================================
# Project: House Prices Prediction
# File: XGBoostHP.py
# Author: Jake Bredice
# Date: 2025-10-24
# Description:
#   Trains an XGBoost model using RandomizedSearchCV-tuned hyperparameters to predict house prices using the Kaggle dataset.
#   Uses DataLoad.py for loading, preprocessing, and feature engineering.
#   Includes evaluation, feature importance visualization, cross-validation, and submission generation.
# =============================================================================

import os
import sys

# Ensure project root is on the path so DataLoad can be imported
script_dir = os.path.dirname(os.path.abspath(__file__))  # Models folder
project_root = os.path.abspath(os.path.join(script_dir, ".."))  # House-Prices folder
if project_root not in sys.path:
    sys.path.append(project_root)


import DataLoad as dl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error, r2_score
import xgboost as xgb

sns.set_style('whitegrid')

# ====== Load and preprocess data ======
train, test = dl.load_datasets()
train_encoded, test_encoded = dl.preprocess_train_test(train, test)

print(f"✅ Data ready. Train shape: {train_encoded.shape}, Test shape: {test_encoded.shape}")

# ====== Separate features and target ======
X = train_encoded.drop(columns=['SalePrice'])
y = train_encoded['SalePrice']

# Train-validation split (80/20) for evaluation
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# ====== Initialize XGBoost Regressor with tuned params ======
xgb_model = xgb.XGBRegressor(
    n_estimators=500,
    learning_rate=0.05,
    max_depth=3,
    subsample=0.9,
    colsample_bytree=0.6,
    min_child_weight=1,
    gamma=2,
    reg_alpha=0.1,
    reg_lambda=1.5,
    random_state=42,
    n_jobs=-1
)

# ====== Train model ======
xgb_model.fit(X_train, y_train)
print("✅ XGBoost trained successfully with tuned parameters!")

# ====== Evaluate model ======
y_pred = xgb_model.predict(X_val)
rmse = np.sqrt(mean_squared_error(y_val, y_pred))
r2 = r2_score(y_val, y_pred)
print(f"📊 Validation RMSE: {rmse:.2f}")
print(f"📈 Validation R² Score: {r2:.4f}")

# ====== Feature Importance ======
importances = pd.Series(xgb_model.feature_importances_, index=X.columns)
top_features = importances.sort_values(ascending=False).head(15)

plt.figure(figsize=(10, 6))
sns.barplot(x=top_features, y=top_features.index)
plt.title("Top 15 Feature Importances (XGBoost)")
plt.xlabel("Importance")
plt.ylabel("Feature")
plt.tight_layout()
plt.show()


# ====== Cross-validation ======
cv_scores = cross_val_score(xgb_model, X, y, cv=5, scoring='neg_root_mean_squared_error')
rmse_scores = -cv_scores
print("5-Fold CV RMSE scores:", rmse_scores)
print(f"Average RMSE: {rmse_scores.mean():.2f}, Std: {rmse_scores.std():.2f}")

# ====== Test Set Predictions & Submission ======
# Align test columns with training features
test_encoded = test_encoded.reindex(columns=X.columns, fill_value=0)
test_preds = xgb_model.predict(test_encoded)

submission = pd.DataFrame({
    'Id': test['Id'],
    'SalePrice': test_preds
})

submission_csv_path = os.path.join(script_dir, 'submissionXGBHP.csv')
submission.to_csv(submission_csv_path, index=False)
print(f"✅ Test predictions generated and saved to {submission_csv_path}")
print(submission.head())