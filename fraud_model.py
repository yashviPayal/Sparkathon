# utils/fraud_model.py

import pandas as pd
import joblib
import numpy as np

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

    # Validate required columns
    missing_cols = [col for col in categorical_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns for fraud detection: {', '.join(missing_cols)}")

    try:
        # Encode categorical columns safely, handling unseen labels
        for col in categorical_cols:
            # Check for unseen labels
            known_labels = encoder.classes_
            # If encoder is multi-label, adjust accordingly. 
            # Here assuming LabelEncoder per column (if not, adjust this logic).
            if col not in df.columns:
                raise ValueError(f"Column {col} missing in input data.")
            unique_vals = df[col].unique()
            unseen = set(unique_vals) - set(known_labels)
            if unseen:
                raise ValueError(f"Unseen labels in column '{col}': {unseen}")
            df[col] = encoder.transform(df[col])
        
        # Scale numeric features
        df_scaled = scaler.transform(df)

        # Predict
        predictions = model.predict(df_scaled)
        df['is_fraud'] = predictions

        return df

    except Exception as e:
        raise RuntimeError(f"Error in fraud prediction: {e}")
