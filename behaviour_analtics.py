# Importing necessary libraries
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
orders = pd.read_csv('/kaggle/input/instacart-market-basket-analysis/orders.csv')
order_products = pd.read_csv('/kaggle/input/instacart-market-basket-analysis/order_products__prior.csv')

# Merge orders and order_products dataframes
order_data = pd.merge(order_products, orders, on='order_id', how='inner')

# Feature Engineering
order_data['order_hour_of_day'] = order_data['order_hour_of_day'].astype(int)
order_data['reordered'] = order_data['reordered'].astype(int)

# Aggregate features at user level
user_features = order_data.groupby('user_id').agg(
    num_orders=('order_id', 'nunique'),
    total_quantity=('reordered', 'sum'),
    avg_order_time=('order_hour_of_day', 'mean')
).reset_index()

# --- Optional: Sample users to speed up processing if data is large ---
# Use this if you want faster results in Kaggle or testing environments
user_features = user_features.sample(n=10000, random_state=42)

# Select features for modeling
features = ['num_orders', 'total_quantity', 'avg_order_time']
X = user_features[features]  # Keep as DataFrame to preserve feature names

# ------------------ Anomaly Detection using Isolation Forest ------------------

# Initialize Isolation Forest with tuned parameters for better performance
model = IsolationForest(
    n_estimators=100,
    max_samples=256,            # Faster, but still representative
    contamination=0.01,
    random_state=42
)

# Fit model
model.fit(X)

# Predict anomalies (1: normal, -1: anomaly)
user_features['anomaly'] = model.predict(X)

# Convert to binary: 0 = normal, 1 = anomaly
user_features['anomaly'] = user_features['anomaly'].map({1: 0, -1: 1})

# Show count of anomalies
print(f"Detected anomalies: {user_features['anomaly'].sum()}")

# ------------------ Visualization ------------------
sns.histplot(user_features['anomaly'], kde=False)
plt.title('Distribution of Anomalies')
plt.xlabel('Anomaly (1 = yes)')
plt.ylabel('User Count')
plt.show()

# ------------------ Dummy Evaluation (optional) ------------------
# Add manual labels for evaluation (just for testing)
user_features['manual_label'] = 0
if user_features['anomaly'].sum() >= 5:  # only if anomalies were found
    sample_anomalies = user_features[user_features['anomaly'] == 1].sample(n=5, random_state=42)
    user_features.loc[sample_anomalies.index, 'manual_label'] = 1


# Evaluation
print("Classification Report:")
print(classification_report(user_features['manual_label'], user_features['anomaly']))

# Confusion matrix
cm = confusion_matrix(user_features['manual_label'], user_features['anomaly'])
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Normal', 'Anomaly'], yticklabels=['Normal', 'Anomaly'])
plt.title('Confusion Matrix')
plt.show()