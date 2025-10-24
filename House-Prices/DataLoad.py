# =============================================================================
# File: DataLoad.py
# Author: Jake Bredice
# Date: 2025-10-24
# Description:
#   Handles loading, preprocessing, and feature engineering for both training and test datasets for the House Prices project.
# =============================================================================

import os
import pandas as pd
import numpy as np

project_root = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(project_root, 'Data')

def load_datasets():
    train_path = os.path.join(data_dir, 'train.csv')
    test_path = os.path.join(data_dir, 'test.csv')

    if not os.path.exists(train_path):
        raise FileNotFoundError(f"❌ train.csv not found in {data_dir}")
    if not os.path.exists(test_path):
        raise FileNotFoundError(f"❌ test.csv not found in {data_dir}")

    train = pd.read_csv(train_path)
    test = pd.read_csv(test_path)
    print(f"✅ Datasets loaded successfully!\nTrain shape: {train.shape}, Test shape: {test.shape}")
    return train, test

def preprocess_data(df):
    # ===== Handle missing values =====
    df['LotFrontage'] = df.groupby('Neighborhood')['LotFrontage'].transform(lambda x: x.fillna(x.median()))
    df['MasVnrType'] = df['MasVnrType'].fillna('None')
    df['MasVnrArea'] = df['MasVnrArea'].fillna(0)

    basement_cat = ['BsmtQual', 'BsmtCond', 'BsmtExposure', 'BsmtFinType1', 'BsmtFinType2']
    for col in basement_cat: df[col] = df[col].fillna('None')
    basement_num = ['BsmtFinSF1', 'BsmtFinSF2', 'BsmtUnfSF', 'TotalBsmtSF', 'BsmtFullBath', 'BsmtHalfBath']
    for col in basement_num: df[col] = df[col].fillna(0)

    garage_cat = ['GarageType', 'GarageFinish', 'GarageQual', 'GarageCond']
    for col in garage_cat: df[col] = df[col].fillna('None')
    garage_num = ['GarageYrBlt']
    for col in garage_num: df[col] = df[col].fillna(0)
    df['GarageCars'] = df['GarageCars'].fillna(0)
    df['GarageArea'] = df['GarageArea'].fillna(0)

    df['Electrical'] = df['Electrical'].fillna(df['Electrical'].mode()[0])
    extreme_missing_cat = ['Alley', 'PoolQC', 'Fence', 'MiscFeature', 'FireplaceQu']
    for col in extreme_missing_cat: df[col] = df[col].fillna('None')

    # ===== Feature Engineering =====
    df['TotalBath'] = df['FullBath'] + 0.5*df['HalfBath'] + df.get('BsmtFullBath',0) + 0.5*df.get('BsmtHalfBath',0)
    df['TotalSF'] = df['1stFlrSF'] + df['2ndFlrSF'] + df.get('TotalBsmtSF',0)
    df['HouseAge'] = df['YrSold'] - df['YearBuilt']
    df['SinceRemodel'] = df['YrSold'] - df['YearRemodAdd']
    df['TotalPorchSF'] = df['OpenPorchSF'] + df['EnclosedPorch'] + df['3SsnPorch'] + df['ScreenPorch']
    df['TotalDeckSF'] = df['WoodDeckSF'] + df['OpenPorchSF']
    df['TotalGarageSF'] = df['GarageArea']
    df['GarageCars_x_Area'] = df['GarageCars'] * df['GarageArea']
    df['LotTotalSF'] = df['LotFrontage'] * df['LotArea']
    df['LotRatio'] = df['LotFrontage'] / df['LotArea']
    df['FireplaceFlag'] = (df['Fireplaces'] > 0).astype(int)
    df['FireplaceScore'] = df['Fireplaces'] * df['FireplaceQu'].replace({'None':0,'Po':1,'Fa':2,'TA':3,'Gd':4,'Ex':5})
    df['Qual_Cond'] = df['OverallQual'] * df['OverallCond']
    df['Qual_x_SF'] = df['OverallQual'] * df['TotalSF']
    df['TotalBath_x_Qual'] = df['TotalBath'] * df['OverallQual']
    df['TotalSF_x_LotArea'] = df['TotalSF'] * df['LotArea']
    df['HasPool'] = (df['PoolQC'] != 'None').astype(int)
    df['HasFence'] = (df['Fence'] != 'None').astype(int)
    df['HasAlley'] = (df['Alley'] != 'None').astype(int)
    df['HasFireplace'] = (df['Fireplaces'] > 0).astype(int)
    df['HasGarage'] = (df['GarageCars'] > 0).astype(int)
    df['TotalBsmtFinSF'] = df.get('BsmtFinSF1',0) + df.get('BsmtFinSF2',0)

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

    # ===== Fix categorical inconsistencies =====
    df['MSZoning'] = df['MSZoning'].replace({'C (all)': 'C'})
    df['Neighborhood'] = df['Neighborhood'].replace({'Names': 'NAmes'})
    df['GarageType'] = df['GarageType'].replace({'Basment': 'Basement'})
    df['RoofStyle'] = df['RoofStyle'].replace({'Gabrel': 'Gambrel'})
    df['Exterior2nd'] = df['Exterior2nd'].replace({'CmentBd': 'CemntBd'})
    df['BldgType'] = df['BldgType'].replace({'Duplx': 'Duplex'})

    return df

def preprocess_train_test(train, test):
    train_processed = preprocess_data(train)
    test_processed = preprocess_data(test)

    # One-hot encode categorical columns
    categorical_cols = train_processed.select_dtypes(include=['object']).columns
    train_encoded = pd.get_dummies(train_processed, columns=categorical_cols, drop_first=True)
    test_encoded = pd.get_dummies(test_processed, columns=categorical_cols, drop_first=True)

    # Align columns
    test_encoded = test_encoded.reindex(columns=train_encoded.columns, fill_value=0)

    return train_encoded, test_encoded

