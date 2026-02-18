import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load
print("Loading data...")
df = pd.read_csv('crop_recommendation.csv')
print(f"Shape: {df.shape}")
print("Columns:", df.columns.tolist())
print(df.head())

# Check classes
print("\nClass distribution:")
print(df['crop'].value_counts())

# Feature Engineering (Same as before)
df['Total_Nutrients'] = df['N'] + df['P'] + df['K']
df['N_Ratio'] = df['N'] / (df['Total_Nutrients'] + 1e-9) 
df['P_Ratio'] = df['P'] / (df['Total_Nutrients'] + 1e-9)
df['K_Ratio'] = df['K'] / (df['Total_Nutrients'] + 1e-9)
df['NP_Ratio'] = df['N'] / (df['P'] + 1e-9)

features = [
    'N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall',
    'Total_Nutrients', 'N_Ratio', 'P_Ratio', 'K_Ratio', 'NP_Ratio'
]
X = df[features]
y = df['crop']

# Encode
le = LabelEncoder()
y_encoded = le.fit_transform(y)
print(f"\nClasses found: {len(le.classes_)}")
print(le.classes_)

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# Scale
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train RF (Baseline)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)
y_pred = model.predict(X_test_scaled)
print(f"\nRandom Forest Accuracy: {accuracy_score(y_test, y_pred) * 100:.2f}%")

print("\n--- Data Inspection ---")
rice_data = df[df['crop'] == 'Rice']
print("Rice Stats:\n", rice_data.describe())

print("\nConfusion Matrix:")
from sklearn.metrics import confusion_matrix
print(confusion_matrix(y_test, y_pred))

print("\nSample Predictions:")
for i in range(10):
    print(f"True: {le.inverse_transform([y_test[i]])[0]}, Pred: {le.inverse_transform([y_pred[i]])[0]}")
