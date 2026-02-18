# 🌾 AgroGuard – Smart Agricultural Decision Support System

AgroGuard is an intelligent web-based agricultural platform that helps farmers make data-driven decisions using **Machine Learning** and **Expert Systems**. It provides crop recommendations, soil health analysis, and flood damage recovery guidance.

---

## ✨ Features

### 🌱 Crop Recommendation System
- ML-powered crop prediction using **Random Forest** classifier
- Takes **Nitrogen (N), Phosphorus (P), Potassium (K)** and **Soil Type** as inputs
- Returns top 5 recommended crops with confidence percentages
- Visual crop cards with images

### 🧪 Soil Health Grading
- Analyzes soil nutrient levels (N, P, K)
- Grades each nutrient as **Low**, **Moderate**, or **High**
- Helps farmers understand soil quality at a glance

### 🌊 Flood Recovery Expert System
- Rule-based expert system for post-flood agricultural recovery
- Analyzes symptoms: water logging, yellow leaves, root rot, soil erosion
- Provides:
  - Root cause analysis
  - Immediate action steps
  - Recommended fertilizers
  - Crops to plant and avoid after flooding

### 🔐 User Authentication
- User signup and login system
- Password recovery functionality
- SQLite-based user management

---

## 🛠️ Tech Stack

| Layer        | Technology                  |
| ------------ | --------------------------- |
| **Backend**  | Python, Flask               |
| **Frontend** | HTML, CSS, JavaScript       |
| **ML Model** | Scikit-learn (Random Forest)|
| **Database** | SQLite                      |
| **Data**     | NumPy, Joblib               |

---

## 📁 Project Structure

```
AgroGuard/
├── app.py                  # Main Flask application
├── train_model.py          # ML model training script
├── generate_data.py        # Dataset generation script
├── database.py             # Database initialization
├── debug_model.py          # Model debugging utilities
├── verify_artifacts.py     # Model artifact verification
├── crop_model.pkl          # Trained Random Forest model
├── label_encoder.pkl       # Crop label encoder
├── scaler.pkl              # Feature scaler
├── soil_encoder.pkl        # Soil type encoder
├── sensor_Crop_Dataset.csv # Training dataset
├── templates/              # HTML templates
│   ├── index_spa.html      # Landing page (SPA)
│   ├── home.html           # Dashboard home
│   ├── login.html          # Login page
│   ├── signup.html         # Registration page
│   ├── soilcheck.html      # Soil analysis page
│   ├── check.html          # Soil check form
│   ├── cropsugg.html       # Crop suggestion results
│   ├── suggesveg.html      # Vegetable suggestions
│   ├── floodrecov.html     # Flood recovery input
│   ├── floodsugg.html      # Flood recovery results
│   ├── about.html          # About page
│   └── fg.html             # Forgot password
├── static/
│   ├── css/                # Stylesheets
│   ├── js/                 # JavaScript files
│   └── images/             # Crop images & assets
└── .gitignore
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/libisanaazrikam/AgroGurad.git
   cd AgroGurad
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate    # On Linux/Mac
   venv\Scripts\activate       # On Windows
   ```

3. **Install dependencies**
   ```bash
   pip install flask numpy scikit-learn joblib
   ```

4. **Initialize the database**
   ```bash
   python database.py
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open in browser**
   ```
   http://127.0.0.1:5000
   ```

---

## 🧠 ML Model Details

- **Algorithm**: Random Forest Classifier
- **Features**: N, P, K, Soil Type (encoded), Total Nutrients, N/P/K Ratios
- **Dataset**: `sensor_Crop_Dataset.csv` with multiple crop classes
- **Training Script**: `train_model.py`

To retrain the model:
```bash
python train_model.py
```

---

## 📸 Screenshots

| Landing Page | Crop Recommendation | Soil Analysis |
|:---:|:---:|:---:|
| Modern SPA landing page | ML-powered crop suggestions | Nutrient grading system |

---

## 👥 Contributors

- **Libisana Azrikam** – Developer

---

## 📄 License

This project is for educational purposes.

---

> Built with ❤️ for smarter farming
