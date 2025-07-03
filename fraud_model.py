# utils/fraud_model.py

import pandas as pd
import joblib

# Load saved model, scaler, and encoder
model = joblib.load("model/fraud_detection_model.pkl")
scaler = joblib.load("model/scaler.pkl")
encoder = joblib.load("model/label_encoder.pkl")

categorical_cols = [
    'payment_method', 'login_location', 'device_type', 'browser_os',
    'cookie_behavior', 'session_token_behavior', 'email_reputation'
]

def predict_fraud(input_df):
    # Copy to avoid modifying original
    df = input_df.copy()

    # Encode categorical columns
    for col in categorical_cols:
        df[col] = encoder.transform(df[col])  # Assumes no unseen labels

    # Scale numeric features
    df_scaled = scaler.transform(df)

    # Predict
    predictions = model.predict(df_scaled)
    df['is_fraud'] = predictions

    return df
