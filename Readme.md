# 👥 Customer Churn Predictor

A full-stack machine learning application that predicts customer churn probability using AI. Built with **Python FastAPI backend**, **React frontend**, and **scikit-learn ML models**.

![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![React](https://img.shields.io/badge/react-18%2B-blue)

---

## 🎯 Project Overview

This application predicts whether a telecom customer will churn (leave the service) based on their characteristics and usage patterns. It provides:

- **Real-time predictions** with probability scores
- **Risk level classification** (Low, Medium, High)
- **Model confidence metrics**
- **Professional recommendations** for retention

Perfect for data science portfolios and demonstrating **ML engineering skills**.

---

## ✨ Features

**AI-Powered Predictions**
- Trained Logistic Regression model with 80%+ accuracy
- Real-time churn probability calculation
- Confidence scores for each prediction

**Professional UI/UX**
- Two-column responsive design
- Clean, modern interface
- Status badges and color-coded results
- Real-time form validation

**Risk Assessment**
- Automatic risk categorization
- Actionable recommendations
- Confidence indicators

**Data Processing**
- Automatic feature scaling
- One-hot encoding for categorical features
- Input validation

---

## 🛠 Tech Stack

### Backend
- **FastAPI** - Modern web framework
- **Python 3.8+** - Programming language
- **scikit-learn** - ML model training & predictions
- **pandas** - Data manipulation
- **MySQL** - Database
- **SQLAlchemy** - ORM

### Frontend
- **React 18** - UI library
- **Axios** - HTTP client
- **CSS3** - Styling
- **Vite** - Build tool

### ML/Data Science
- **scikit-learn** - Model training
- **pandas** - Data processing
- **numpy** - Numerical computations
- **joblib** - Model serialization

---

## 📊 Dataset

- **Source**: Telecom Customer Churn Dataset (Kaggle)
- **Rows**: 7,043 customer records
- **Features**: 30 (after preprocessing)
- **Target**: Churn (binary: Yes/No)
- **Class Distribution**: 73% No Churn, 27% Churn (imbalanced)

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Node.js 14+
- MySQL 8.0+
- Git

### Installation

#### 1. Backend Setup

```bash
# Navigate to project directory
cd Customer-Churn-Predictor

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup MySQL database
mysql -u root -p
> CREATE DATABASE churn_db;
> EXIT;

# Load data and train model
python src/train.py
```

#### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd churn-predictor-frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### Running the Application

**Terminal 1 - Backend:**
```bash
cd Customer-Churn-Predictor
venv\Scripts\activate  # or source venv/bin/activate
uvicorn api.main:app --reload
```

Backend runs on: `http://localhost:8000`

**Terminal 2 - Frontend:**
```bash
cd churn-predictor-frontend
npm run dev

Frontend runs on: `http://localhost:5173`

---

## 📁 Project Structure
Customer-Churn-Predictor/

├── api/
│   ├── init.py
│   └── main.py              # FastAPI application

├── src/
│   ├── init.py
│   ├── data_loader.py       # Database connection
│   ├── preprocessing.py     # Data cleaning
│   ├── feature_engineering.py  # Feature processing
│   └── train.py             # Model training

├── models/
│   ├── churn_model.pkl      # Trained model
│   └── scaler.pkl           # Feature scaler

├── dataset/
│   └── WA_Fn-UseC_-Telco-Customer-Churn.csv

├── notebooks/
│   └── EDA.ipynb            # Exploratory Data Analysis

├── churn-predictor-frontend/
│   ├── src/
│   │   ├── App.jsx          # Main React component
│   │   ├── App.css          # Styling
│   │   ├── index.css        # Global styles
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js

├── .env
├── .gitignore
└── README.md

---

## 🤖 How It Works

### 1. Data Pipeline
Raw CSV → MySQL Database → Preprocessing → Feature Engineering → Scaling

### 2. Model Training
Training Data (80%) → Logistic Regression → Model Evaluation → Save Model

Test Data (20%)     ↓

Metrics (Accuracy, Precision, Recall, F1)

### 3. Prediction Flow
User Input → FastAPI Endpoint → Feature Transformation → Model Prediction → Risk Classification → Response

### 4. Frontend Processing
Form Input → Validation → API Call → Result Display → Recommendations

---

## 📈 Model Performance

| Metric | Score |
|--------|-------|
| **Accuracy** | 80.38% |
| **Precision** | 64.75% |
| **Recall** | 57.49% |
| **F1-Score** | 60.91% |
| **ROC-AUC** | 0.8356 |

**Model**: Logistic Regression (chosen over Random Forest & XGBoost for best F1-score)

---

## 🔄 API Endpoints

### `/predict` (POST)
Predict churn probability for a customer.

**Request:**
```json
{
  "tenure": 12,
  "monthly_charges": 70,
  "total_charges": 840,
  "has_partner": "no",
  "has_dependents": "no",
  "internet_type": "dsl",
  "contract_type": "month_to_month"
}
```

**Response:**
```json
{
  "churn_probability": 45.23,
  "risk_level": "MEDIUM",
  "prediction": "CHURN",
  "confidence": 76.45
}
```

### `/health` (GET)
Check API status.
GET http://localhost:8000/health

---

## 🧪 Testing

### Test Scenarios

**Low Risk Customer:**
Tenure: 60 months

Contract: 2 years

Monthly: $65

→ Expected: LOW RISK 

**High Risk Customer:**
Tenure: 2 months

Contract: Month-to-month

Monthly: $85

→ Expected: HIGH RISK 

---

## 📚 What I Learned

✅ Full-stack development (frontend + backend)
✅ ML model training & evaluation
✅ REST API design with FastAPI
✅ React hooks & state management
✅ Database design with MySQL
✅ Feature engineering & preprocessing
✅ Model serialization & deployment
✅ Responsive UI design
✅ Error handling & validation

---

## Future Enhancements

- [ ] Add prediction history & export to CSV
- [ ] Customer segmentation analysis
- [ ] Time-series analysis for trend prediction
- [ ] Advanced ML models (XGBoost, Neural Networks)
- [ ] User authentication & authorization
- [ ] Batch prediction processing
- [ ] Dashboard with analytics
- [ ] Model versioning & A/B testing
- [ ] Docker containerization
- [ ] CI/CD pipeline

---

## Acknowledgments

- Dataset from Kaggle
- FastAPI documentation
- React best practices
- scikit-learn community

---

**Author: Muhammad Hashir Khan**

