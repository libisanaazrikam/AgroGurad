import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
import random
import os

# Set seeds
np.random.seed(42)
random.seed(42)
os.environ['PYTHONHASHSEED'] = str(42)

print("Loading dataset...")
# Load the dataset
print("Loading dataset...")
df = pd.read_csv('sensor_Crop_Dataset.csv')

# Rename columns
df = df.rename(columns={
    'Nitrogen': 'N',
    'Phosphorus': 'P',
    'Potassium': 'K',
    'Crop': 'label',
    'Soil_Type': 'soil_type'
})

# Encode Soil Type
print("Encoding Soil Type...")
soil_le = LabelEncoder()
df['soil_type_encoded'] = soil_le.fit_transform(df['soil_type'])

# --- Feature Engineering ---
print("Generating features...")
df['Total_Nutrients'] = df['N'] + df['P'] + df['K']
df['N_Ratio'] = df['N'] / (df['Total_Nutrients'] + 1e-9) 
df['P_Ratio'] = df['P'] / (df['Total_Nutrients'] + 1e-9)
df['K_Ratio'] = df['K'] / (df['Total_Nutrients'] + 1e-9)
df['NP_Ratio'] = df['N'] / (df['P'] + 1e-9)

# Select features
features = [
    'N', 'P', 'K', 'soil_type_encoded',
    'Total_Nutrients', 'N_Ratio', 'P_Ratio', 'K_Ratio', 'NP_Ratio'
]
X = df[features]
y = df['label']

# Encode Labels
print("Encoding labels...")
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# Split 80% Train, 20% Test
print("Splitting data (80% Train / 20% Test)...")
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# Scaling
print("Scaling features...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train XGBoost
print("Training XGBoost Model...")
model = XGBClassifier(
    n_estimators=300,
    learning_rate=0.05,
    max_depth=5,
    subsample=0.8,
    colsample_bytree=0.8,
    n_jobs=-1,
    random_state=42,
    eval_metric='mlogloss'
)

model.fit(X_train_scaled, y_train)

# Evaluate
y_pred = model.predict(X_test_scaled)
acc = accuracy_score(y_test, y_pred)
print(f"\nFinal Test Accuracy: {acc * 100:.2f}%")

# Cross Validation check
scores = cross_val_score(model, X_train_scaled, y_train, cv=5)
print(f"Cross-Validation Average: {scores.mean() * 100:.2f}%")

# Save
print("Saving artifacts...")
joblib.dump(model, 'crop_model.pkl')
joblib.dump(le, 'label_encoder.pkl')
joblib.dump(scaler, 'scaler.pkl')
joblib.dump(soil_le, 'soil_encoder.pkl')
print("Done!")
