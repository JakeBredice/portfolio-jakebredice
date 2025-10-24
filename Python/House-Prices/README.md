# House Prices Prediction Project

## Overview
This project predicts house prices using the Kaggle House Prices dataset. It includes data loading, preprocessing, feature engineering, and training of multiple models, including Gradient Boosting and XGBoost. Special engineered features like `Qual_x_SF` were created to improve predictive performance.

## Data Preprocessing & Feature Engineering

My data preprocessing and feature engineering leveraged both domain expertise and statistical reasoning to improve model performance and interpretability.

### Domain Insights
Through conversations with my father, a real-estate appraiser, I identified which aspects of a home are most likely to influence buyers’ perceptions. This informed several engineered features, including:

- **TotalBath**: Combined all full and half baths (including basement baths) to reflect total bathroom value.
- **TotalSF**: Sum of first floor, second floor, and basement square footage to capture total living space.
- **GarageCars_x_Area**: Interaction of garage size and capacity.
- **LotTotalSF** and **LotRatio**: Represent overall lot area and frontage ratio.
- **Boolean flags**: `HasPool`, `HasFence`, `HasAlley`, `HasFireplace`, `HasGarage` to separate presence effects from magnitude.

### AestheticComposite
I created a feature called **AestheticComposite** to reflect what I hypothesized would be most important to buyers from an aesthetic standpoint:

```python
# ====== AestheticComposite Feature ======
    # Convert categorical quality ratings to numeric for calculation
    qual_map = {'Ex': 5, 'Gd': 4, 'TA': 3, 'Fa': 2, 'Po': 1, 'None': 0}

    # Ensure the columns exist (Exterior/Kitchen/Fireplace)
    df['ExteriorQual_num'] = df['ExterQual'].map(qual_map)
    df['ExterCond_num'] = df['ExterCond'].map(qual_map)
    df['KitchenQual_num'] = df['KitchenQual'].map(qual_map)
    df['FireplaceScore_num'] = df['Fireplaces'] * df['FireplaceQu'].replace(qual_map)

    # AestheticComposite formula
    df['AestheticComposite'] = (0.5 * df['ExteriorQual_num']) + (2 * df['ExterCond_num']) + df['KitchenQual_num'] + df['FireplaceScore_num']

    # Drop temporary numeric columns 
    df.drop(columns=['ExteriorQual_num', 'ExterCond_num', 'KitchenQual_num', 'FireplaceScore_num'], inplace=True)
```

## Models
For predicting house prices, multiple tree-based models were trained and evaluated. All models used `RandomizedSearchCV` to optimize hyperparameters for better predictive performance.

- **Random Forest (RF)**: Served as a baseline model. RF provided strong performance with lower risk of overfitting and helped guide expectations for more complex models.

- **Gradient Boosting (GB)**: Improved on the RF baseline by sequentially correcting errors from previous trees. GB captured complex relationships between features and sale price.

- **XGBoost (XGB)**: Delivered the best performance among all models. Like GB, it uses gradient boosting but includes additional regularization and optimized tree learning, which helped achieve the lowest validation RMSE and highest R² scores.

Each model’s performance was evaluated using RMSE and R² on a validation set, and top feature importances were visualized to understand which factors most influenced predicted sale prices.

## How to Run
1. Place `train.csv` and `test.csv` in the `Data/` folder.
2. Place `DataLoad.py` in the `House-Prices/` folder.
3. Run any model script from the `Models/` folder:
   ```bash
   python Models/GradientBoostHP.py
   python Models/XGBoostHP.py
   ```
## Summary & Lessons Learned
Through this project, I combined domain expertise, statistical reasoning, and machine learning techniques to improve predictive accuracy for house prices. Key takeaways include:

- **Feature Engineering Matters:** Creating features like `TotalBath`, `TotalSF`, `GarageCars_x_Area`, and `AestheticComposite` helped the models capture complex relationships between home characteristics and sale price.  
- **Domain Expertise is Valuable:** Conversations with my father, a real-estate appraiser, informed which aspects of a home buyers perceive as valuable, guiding the design of engineered features.  
- **Baseline Models are Important:** Using Random Forest as a baseline provided a reference point for evaluating more complex models like Gradient Boosting and XGBoost.  
- **Model Tuning Improves Performance:** RandomizedSearchCV helped optimize hyperparameters, improving RMSE and R² while balancing model complexity and overfitting risk.  
- **Iterative Process:** Experimenting with feature combinations, interactions, and composite scores reinforced the importance of systematic testing and validation.  
- **Interpretable Insights:** Feature importance visualization helped understand which home characteristics most strongly influence predicted sale prices, providing actionable insights beyond pure prediction.  

This project reinforced my ability to merge domain knowledge with data science, and demonstrates a full ML/Analytics workflow from data preprocessing to model evaluation and interpretation.

### Link to Kaggle Competition:
https://www.kaggle.com/competitions/house-prices-advanced-regression-techniques/overview