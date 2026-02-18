from flask import Flask, render_template, url_for, request, redirect, flash
import sqlite3
import joblib
import numpy as np

app = Flask(__name__)
app.secret_key = "replace_with_a_secret_key"

# Load trained ML model + label encoder
model = joblib.load('crop_model.pkl')
le = joblib.load('label_encoder.pkl')
scaler = joblib.load('scaler.pkl')
soil_le = joblib.load('soil_encoder.pkl') # Load Soil Encoder

# Map crops → images
CROP_IMAGE_MAP = {
    'rice': "images/rice.jpeg",
    'maize': "images/maize.jpg",
    'chickpea': "images/chilly.jpeg",
    'kidneybeans': "images/rice.jpeg",
    'banana': "images/banana.jpg",
    'apple': "images/apple.jpg",
    'pomegranate': "images/pomergranate.jpeg",
    'muskmelon': "images/muskmelon.jpg",
    'papaya': "images/papaya.jpeg",
    'mango': "images/mango.jpg",
    'mothbeans': "images/mothbeans.jpeg",
    'mungbean': "images/mungbean.jpeg",
    'jute': "images/jute.jpg",
    'blackgram': "images/blackgram.jpg",
    'coconut': "images/coconut.jpg",
    'watermelon': "images/watermelon.jpeg",
    'coffee': "images/coffee.jpeg",
    'cotton': "images/Cotton.jpg",
    'grapes': "images/grapes.jpg",
    'orange': "images/Orange.jpg",
    'pigeonpeas': "images/pigeonpeas.jpeg",
    'lentil': "images/lentil.jpeg"
}

DB_PATH = 'database.db'

# ---------- DB Helpers ----------
def insert_user(username, password, phone, location):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password, phone, location) VALUES (?, ?, ?, ?)",
                   (username, password, phone, location))
    conn.commit()
    conn.close()

def validate_login(username, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user is not None

# ---------- Soil Grading ----------
def get_soil_grade(N, P, K):
    def classify(value, low, high):
        if value < low:
            return "Low"
        elif value > high:
            return "High"
        else:
            return "Moderate"

    N_grade = classify(N, 50, 100)
    P_grade = classify(P, 30, 60)
    K_grade = classify(K, 30, 60)

    return N_grade, P_grade, K_grade

# ---------- Flood Expert System ----------
def analyze_flood_damage(symptoms, description):
    analysis_report = {
        "problem": "Flood damage detected.",
        "reasons": [],
        "immediate_actions": [],
        "prevention": [],
        "fertilizers": [],
        "crops_to_plant": [],
        "crops_to_avoid": []
    }

    # Rule-based logic
    if "water_logging" in symptoms:
        analysis_report["reasons"].append("Water stagnation caused oxygen deprivation in roots (Hypoxia).")
        analysis_report["immediate_actions"].append("Drain excess water immediately using trenches or pumps.")
        analysis_report["immediate_actions"].append("Aerate the soil by light tilling once it dries slightly.")
        analysis_report["prevention"].append("Install better drainage systems or raised beds.")
        analysis_report["crops_to_avoid"].append("Maize (highly sensitive to waterlogging)")
        analysis_report["crops_to_plant"].append("Rice (if water persists)")
        analysis_report["crops_to_plant"].append("Jute")

    if "yellow_leaves" in symptoms:
        analysis_report["reasons"].append("Nitrogen leaching due to excess water (Chlorosis).")
        analysis_report["immediate_actions"].append("Apply Nitrogen-rich fertilizers (Urea or Ammonium Sulphate).")
        analysis_report["fertilizers"].append("Urea")
        analysis_report["fertilizers"].append("NPK 20-20-20 (foliar spray)")

    if "root_rot" in symptoms:
        analysis_report["reasons"].append("Fungal infection due to prolonged wetness.")
        analysis_report["immediate_actions"].append("Apply fungicides (e.g., Copper Oxychloride) near the root zone.")
        analysis_report["crops_to_avoid"].append("Root vegetables (Carrots, Potatoes)")

    if "soil_erosion" in symptoms:
        analysis_report["reasons"].append("Topsoil washed away, losing organic matter.")
        analysis_report["immediate_actions"].append("Add organic compost or manure to restore structure.")
        analysis_report["prevention"].append("Plant cover crops (like Clover or Vetch) to hold soil.")

    # Defaults if no specific symptoms
    if not analysis_report["immediate_actions"]:
        analysis_report["immediate_actions"].append("Monitor soil moisture levels daily.")
        analysis_report["immediate_actions"].append("Remove debris and dead plant material to prevent disease.")
    
    if not analysis_report["crops_to_plant"]:
        analysis_report["crops_to_plant"] = ["Mungbean", "Short-duration Pulses", "Spinach"]

    return analysis_report


# ---------- Routes ----------
@app.route('/')
def main():
    return render_template("index_spa.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if validate_login(username, password):
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')
# Dashboard
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('dashboard.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        phone = request.form['phone']
        location = request.form['location']
        insert_user(username, password, phone, location)
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/soilcheck')
def soilcheck():
    return render_template('soilcheck.html')

@app.route('/check', methods=['GET'])
def check_page():
    return render_template('check.html')

# Soil Grading only
@app.route('/soilgrade', methods=['POST'])
def soilgrade():
    try:
        N = float(request.form['N'])
        P = float(request.form['P'])
        K = float(request.form['K'])

        N_grade, P_grade, K_grade = get_soil_grade(N, P, K)

        return {
            'N_grade': N_grade,
            'P_grade': P_grade,
            'K_grade': K_grade,
            'N': N, 'P': P, 'K': K
        }
    except Exception as e:
        return {'error': str(e)}, 400

# Crop Recommendation
@app.route('/suggesveg', methods=['POST'])
def suggesveg():
    try:
        N = float(request.form['N'])
        P = float(request.form['P'])
        K = float(request.form['K'])
        soil_type = request.form['soil_type'] # Get Soil Type

        # Encode Soil Type
        try:
             soil_encoded = soil_le.transform([soil_type])[0]
        except ValueError:
             # Handle unseen labels or default
             soil_encoded = 0 # Default/Fallback

        # Feature Engineering (Must match training!)
        total_nutrients = N + P + K
        n_ratio = N / (total_nutrients + 1e-9)
        p_ratio = P / (total_nutrients + 1e-9)
        k_ratio = K / (total_nutrients + 1e-9)
        np_ratio = N / (P + 1e-9)

        # Features: N, P, K, soil_type_encoded, Total_Nutrients, N_Ratio, P_Ratio, K_Ratio, NP_Ratio
        features = np.array([[N, P, K, soil_encoded, total_nutrients, n_ratio, p_ratio, k_ratio, np_ratio]])
        
        input_data_scaled = scaler.transform(features)

        if hasattr(model, "predict_proba"):
            probs = model.predict_proba(input_data_scaled)[0]
            crop_names = list(le.classes_)
            recommendations = []
            for i, crop in enumerate(crop_names):
                prob = float(probs[i])
                img = CROP_IMAGE_MAP.get(crop, None)
                recommendations.append({'name': crop, 'prob': round(prob * 100, 2), 'img': img})
            recommendations.sort(key=lambda x: x['prob'], reverse=True)
            # Filter top results if too many
            recommendations = recommendations[:5]
        else:
            pred_index = model.predict(input_data_scaled)[0]
            pred_name = le.inverse_transform([pred_index])[0]
            recommendations = [{'name': pred_name, 'prob': 100.0, 'img': CROP_IMAGE_MAP.get(pred_name, None)}]

        return {'recommendations': recommendations}

    except Exception as e:
        return {'error': str(e)}, 400

@app.route('/floodrecov')
def floodrecov():
    return render_template('index_spa.html')

@app.route('/analyze_flood', methods=['POST'])
def analyze_flood():
    try:
        data = request.json
        symptoms = data.get('symptoms', [])
        description = data.get('description', '')
        
        result = analyze_flood_damage(symptoms, description)
        
        return result
    except Exception as e:
        return {'error': str(e)}, 500

@app.route('/cropsugg', methods=['GET', 'POST'])
def cropsugg():
    if request.method == 'POST':
        N = request.form.get('N')
        P = request.form.get('P')
        K = request.form.get('K')
        return render_template('cropsugg.html', N=N, P=P, K=K)
    return render_template('cropsugg.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/fg', methods=['GET', 'POST'])
def fg():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm = request.form['confirm']

        if password != confirm:
            flash("Passwords do not match!")
            return render_template('fg.html')

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET password=? WHERE username=?", (password, username))
        conn.commit()
        conn.close()

        flash("Password updated successfully!")
        return redirect(url_for('login'))

    return render_template('fg.html')

# ---------- Run ----------
if __name__ == '__main__':
    app.run(debug=True)
