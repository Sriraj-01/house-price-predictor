# 🏠 House Price Predictor (End-to-End ML System)

An end-to-end **House Price Prediction system** built using **Machine Learning, Flask, and React**, covering the complete ML lifecycle — from data preprocessing and feature engineering to model deployment and a production-ready web interface.

This project demonstrates how a real-world ML model is trained, served as an API, and consumed by a modern frontend application.

---

## 🔗 Live Demo

- **Frontend (React + Netlify):**  
  https://stirring-gumdrop-fcd1e1.netlify.app

- **Backend API (Flask + Render):**  
  https://house-price-api-7f6w.onrender.com

---

## 🧠 Problem Statement

Predict the **market price of residential properties** based on features such as:
- Location
- BHK
- Carpet Area
- Floor
- Bathrooms & Balconies
- Furnishing, Ownership, Transaction type, etc.

This is a **regression problem** trained on a large real-estate dataset with extensive cleaning and feature engineering.

---

## 🏗️ Project Architecture
house-price-predictor/
│
├── backend/ # Flask ML API
│ ├── app.py
│ ├── requirements.txt
│ └── model/
│ └── house_price_model.pkl
│
├── frontend/ # React (Vite) frontend
│ ├── src/
│ ├── public/
│ ├── package.json
│ └── vite.config.js
│
├── ml_pipeline/ # ML training pipeline
│ ├── cleaning.py
│ ├── feature_engineering.py
│ ├── train_model.py
│ └── utils.py
│
├── .gitignore
└── README.md


---

## ⚙️ Tech Stack

### 🔹 Machine Learning
- Python
- Pandas, NumPy
- Scikit-learn
- XGBoost
- Feature Engineering & Pipelines

### 🔹 Backend
- Flask (REST API)
- Joblib (model serialization)
- Render (deployment)

### 🔹 Frontend
- React (Vite)
- Axios
- Netlify (deployment)

---

## 📊 Model Performance

Final trained model metrics on test data:

- **MAE:** ₹1.25M  
- **RMSE:** ₹2.86M  
- **R² Score:** 0.92  

The model generalizes well on unseen data and captures key pricing patterns.

---

## 🚀 API Usage

### Endpoint


### Sample Request (JSON)
```json
{
  "location": "Mumbai",
  "Carpet Area": 900,
  "Floor": 5,
  "Bathroom": 2,
  "Balcony": 1,
  "BHK": 2,
  "Status": "Ready to Move",
  "Transaction": "Resale",
  "Furnishing": "Semi-Furnished",
  "Ownership": "Freehold"
}

{
  "predicted_price": 5576622.0
}
```

🛠️ Local Setup :     
Backend >     
cd backend    
pip install -r requirements.txt     
python app.py       

Frontend >     
cd frontend      
npm install     
npm run dev      


👤 Author     
Sriraj Yamana      
Aspiring Machine Learning Engineer
