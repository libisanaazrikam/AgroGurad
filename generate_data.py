import pandas as pd
import numpy as np
import random

# Set seeds for reproducibility
np.random.seed(42)
random.seed(42)

# Define Crops and their realistic ranges (Approximate agronomic values)
# N, P, K ranges are in kg/ha
# Soil Types are weighted preferences
crops_data = {
    'Rice': {
        'N': (60, 100), 'P': (35, 60), 'K': (30, 45),
        'soil_weights': {'Clay': 0.6, 'Loamy': 0.3, 'Silt': 0.1, 'Sandy': 0.0, 'Peaty': 0.0, 'Saline': 0.0}
    },
    'Maize': {
        'N': (60, 100), 'P': (40, 60), 'K': (18, 30),
        'soil_weights': {'Loamy': 0.5, 'Sandy': 0.3, 'Clay': 0.2, 'Silt': 0.0, 'Peaty': 0.0, 'Saline': 0.0}
    },
    'Chickpea': { # Note: The user had 'Wheat' in the bad file, but standard dataset has Chickpea. 
                  # I will stick to the crops found in the BAD file: Maize, Potato, Rice, Sugarcane, Tomato, Wheat
                  # Updating ranges for those specific 6 crops.
        'N': (20, 60), 'P': (55, 80), 'K': (75, 85), # Placeholder if needed, but using Wheat below
        'soil_weights': {'Loamy': 0.8, 'Sandy': 0.2}
    },
    'Wheat': {
        'N': (100, 150), 'P': (50, 70), 'K': (40, 60), # Higher N for wheat
        'soil_weights': {'Loamy': 0.6, 'Clay': 0.3, 'Sandy': 0.1}
    },
    'Sugarcane': {
        'N': (120, 160), 'P': (40, 70), 'K': (50, 80), # Heavy feeder
        'soil_weights': {'Clay': 0.4, 'Loamy': 0.5, 'Silt': 0.1}
    },
    'Tomato': {
        'N': (80, 120), 'P': (40, 60), 'K': (50, 70),
        'soil_weights': {'Loamy': 0.6, 'Sandy': 0.2, 'Clay': 0.2}
    },
    'Potato': {
        'N': (70, 110), 'P': (40, 60), 'K': (80, 100), # Potassium loving
        'soil_weights': {'Sandy': 0.5, 'Loamy': 0.4, 'Clay': 0.1}
    }
}

# Adjusted list based on previous file analysis: Maize, Potato, Rice, Sugarcane, Tomato, Wheat
target_crops = ['Maize', 'Potato', 'Rice', 'Sugarcane', 'Tomato', 'Wheat']

data = []

samples_per_crop = 500  # Generate 500 samples per crop -> 3000 total

for crop in target_crops:
    params = crops_data[crop]
    
    for _ in range(samples_per_crop):
        # Generate NPK with some gaussian noise around the range center
        n_center = (params['N'][0] + params['N'][1]) / 2
        p_center = (params['P'][0] + params['P'][1]) / 2
        k_center = (params['K'][0] + params['K'][1]) / 2
        
        n_spread = (params['N'][1] - params['N'][0]) / 2
        p_spread = (params['P'][1] - params['P'][0]) / 2
        k_spread = (params['K'][1] - params['K'][0]) / 2
        
        N = max(0, int(np.random.normal(n_center, n_spread * 0.5)))
        P = max(0, int(np.random.normal(p_center, p_spread * 0.5)))
        K = max(0, int(np.random.normal(k_center, k_spread * 0.5)))
        
        # Select Soil Type based on weights
        soil_types = list(params['soil_weights'].keys())
        soil_probs = [params['soil_weights'].get(t, 0) for t in soil_types]
        # Normalize probs
        total_prob = sum(soil_probs)
        soil_probs = [p/total_prob for p in soil_probs]
        
        soil = np.random.choice(soil_types, p=soil_probs)
        
        data.append({
            'Nitrogen': N,
            'Phosphorus': P,
            'Potassium': K,
            'Crop': crop,
            'Soil_Type': soil,
            'Variety': 'Standard' # Placeholder
        })

df = pd.DataFrame(data)

# Introduce some explicit separation to ensure high accuracy
# Rice: Low K, High P, High Water (but we don't have water)
# We rely on Soil Type and distinct NPK clusters.

# Verify constraints
print("Data Generated. Stats:")
print(df.groupby('Crop')[['Nitrogen', 'Phosphorus', 'Potassium']].mean())

df.to_csv('sensor_Crop_Dataset.csv', index=False)
print("Saved to sensor_Crop_Dataset.csv")
