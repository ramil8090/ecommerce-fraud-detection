#!/usr/bin/env python

import pickle

import pandas as pd
import numpy as np
import sklearn


from sklearn.feature_extraction import DictVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline


print(f'pandas=={pd.__version__}')
print(f'numpy=={np.__version__}')
print(f'sklearn=={sklearn.__version__}')

model_path = './models/pipeline.bin'

def load_data():
    data_url = './data/kaggle.com/umuttuygurr/e-commerce-fraud-detection-dataset/transactions.csv'

    df = pd.read_csv(data_url)

    # Parse transaction time to extract derived data
    df['transaction_time'] = pd.to_datetime(df['transaction_time'], errors='coerce')
    df['day'] = df['transaction_time'].dt.dayofweek
    df['month'] = df['transaction_time'].dt.month
    df['hour'] = df['transaction_time'].dt.hour
    # Define night hours (e.g., 10 PM to 5 AM)
    df['night_hours'] = ((df['hour'] >= 22) | (df['hour'] < 5)).astype(int)

    # Drop unnecessary columns
    del df['transaction_id']
    del df['user_id']
    del df['transaction_time']

    return df




def train_model(df):
    categorical = [
        'country', 
        'bin_country', 
        'channel', 
        'merchant_category', 
        'promo_used', 
        'avs_match', 
        'cvv_result', 
        'three_ds_flag', 
        'night_hours'
    ]
    numerical = [
        'account_age_days', 
        'total_transactions_user', 
        'avg_amount_user', 
        'amount', 
        'shipping_distance_km', 
        'month', 
        'day', 
        'hour'
    ]


    y_train = df.is_fraud
    train_dict = df[categorical + numerical].to_dict(orient='records')

    pipeline = make_pipeline(
        DictVectorizer(),
        RandomForestClassifier(n_estimators=200,
                                max_depth=9,
                                min_samples_leaf=5,
                                random_state=1)
    )

    pipeline.fit(train_dict, y_train)

    return pipeline


def save_model(pipeline, output_file):
    with open(output_file, 'wb') as f_out:
        pickle.dump(pipeline, f_out)



df = load_data()
pipeline = train_model(df)
save_model(pipeline, model_path)

print(f'Model saved to {model_path}')