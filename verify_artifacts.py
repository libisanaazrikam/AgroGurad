import joblib
import numpy as np
import pandas as pd

print("Loading artifacts...")
try:
    model = joblib.load('crop_model.pkl')
    le = joblib.load('label_encoder.pkl')
    scaler = joblib.load('scaler.pkl')
    soil_le = joblib.load('soil_encoder.pkl')
    print("Artifacts loaded successfully.")
    
    print(f"Model type: {type(model)}")
    print(f"Scaler mean shape: {scaler.mean_.shape}")
    print(f"Soil Classes: {soil_le.classes_}")
    
    # Test prediction vector
    # Features: N, P, K, soil_encoded, Total, N_Ratio, P_Ratio, K_Ratio, NP_Ratio
    # 9 Features
    test_features = np.zeros((1, 9))
    print(f"Testing prediction with shape {test_features.shape}...")
    
    pred = model.predict(test_features)
    print(f"Prediction success: {pred}")

except Exception as e:
    print(f"ERROR: {e}")
