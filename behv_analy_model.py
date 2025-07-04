import pandas as pd
from sklearn.ensemble import IsolationForest

def run_isolation_forest(order_data_df):
    """
    Runs Isolation Forest anomaly detection on aggregated user order data.

    Args:
        order_data_df (pd.DataFrame): DataFrame with columns:
                                      'order_id', 'order_hour_of_day', 'reordered', 'user_id'

    Returns:
        pd.DataFrame: user_features DataFrame with 'anomaly' column added (0=normal, 1=anomaly)
    """
    order_data_df['order_hour_of_day'] = order_data_df['order_hour_of_day'].astype(int)
    order_data_df['reordered'] = order_data_df['reordered'].astype(int)

    user_features = order_data_df.groupby('user_id').agg(
        num_orders=('order_id', 'nunique'),
        total_quantity=('reordered', 'sum'),
        avg_order_time=('order_hour_of_day', 'mean')
    ).reset_index()

    features = ['num_orders', 'total_quantity', 'avg_order_time']
    X = user_features[features]

    model = IsolationForest(
        n_estimators=100,
        max_samples=256,
        contamination=0.01,
        random_state=42
    )
    model.fit(X)

    user_features['anomaly'] = model.predict(X)
    user_features['anomaly'] = user_features['anomaly'].map({1: 0, -1: 1})

    return user_features
