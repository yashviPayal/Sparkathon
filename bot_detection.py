import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Load dataset (✅ Fixed Windows path with raw string)
df = pd.read_csv(r"C:\Users\hp\Downloads\bot_human_behavior_dataset.csv")

# 2. Explore the data
print("First 5 rows:")
print(df.head())

print("\nMissing values per column:")
print(df.isnull().sum())

# 3. Preprocess categorical/boolean columns
df['paste_detected'] = df['paste_detected'].astype(int)
df['user_agent_contains_bot'] = df['user_agent_contains_bot'].astype(int)
df['navigator_webdriver'] = df['navigator_webdriver'].astype(int)

# 4. Separate features and label
X = df.drop("label", axis=1)
y = df["label"]

# 5. Normalize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 6. Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# 7. Train model
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# 8. Evaluate model
y_pred = clf.predict(X_test)

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# 9. Plot feature importances
feat_importances = pd.Series(clf.feature_importances_, index=X.columns)
plt.figure(figsize=(10, 6))
sns.barplot(x=feat_importances.values, y=feat_importances.index)
plt.title("Feature Importances")
plt.xlabel("Importance Score")
plt.ylabel("Features")
plt.tight_layout()
plt.show()
