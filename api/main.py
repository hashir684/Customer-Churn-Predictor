import joblib
import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Churn Predictor API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChurnPredictionRequest(BaseModel):
    """Simple input that React can send"""
    tenure: float
    monthly_charges: float
    total_charges: float
    has_partner: str = "no"  # yes/no
    has_dependents: str = "no"  # yes/no
    internet_type: str = "dsl"  # dsl/fiber/no
    contract_type: str = "month_to_month"  # month_to_month/one_year/two_year

model = joblib.load('models/churn_model.pkl')
scaler = joblib.load('models/scaler.pkl')

feature_names = list(scaler.feature_names_in_)

defaults = {
    'SeniorCitizen': 0,
    'Partner': 0,
    'Dependents': 0,
    'tenure': 0,
    'PhoneService': 1,
    'PaperlessBilling': 0,
    'MonthlyCharges': 0,
    'TotalCharges': 0,
    'gender_Male': 1,
    'MultipleLines_No phone service': 1,
    'MultipleLines_Yes': 0,
    'InternetService_Fiber optic': 0,
    'InternetService_No': 0,
    'OnlineSecurity_No internet service': 1,
    'OnlineSecurity_Yes': 0,
    'OnlineBackup_No internet service': 1,
    'OnlineBackup_Yes': 0,
    'DeviceProtection_No internet service': 1,
    'DeviceProtection_Yes': 0,
    'TechSupport_No internet service': 1,
    'TechSupport_Yes': 0,
    'StreamingTV_No internet service': 1,
    'StreamingTV_Yes': 0,
    'StreamingMovies_No internet service': 1,
    'StreamingMovies_Yes': 0,
    'Contract_One year': 0,
    'Contract_Two year': 0,
    'PaymentMethod_Credit card (automatic)': 1,
    'PaymentMethod_Electronic check': 0,
    'PaymentMethod_Mailed check': 0
}

def convert_yes_no(value: str) -> int:
    return 1 if value.lower() == 'yes' else 0

def get_internet_features(internet_type: str) -> dict:
    """Convert internet type to one-hot encoded features"""
    internet_type = internet_type.lower()
    if internet_type == 'fiber':
        return {'InternetService_Fiber optic': 1, 'InternetService_No': 0}
    elif internet_type == 'no':
        return {'InternetService_Fiber optic': 0, 'InternetService_No': 1}
    else:  # dsl
        return {'InternetService_Fiber optic': 0, 'InternetService_No': 0}

def get_contract_features(contract_type: str) -> dict:
    """Convert contract type to one-hot encoded features"""
    contract_type = contract_type.lower()
    if contract_type == 'one_year':
        return {'Contract_One year': 1, 'Contract_Two year': 0}
    elif contract_type == 'two_year':
        return {'Contract_One year': 0, 'Contract_Two year': 1}
    else:  # month_to_month
        return {'Contract_One year': 0, 'Contract_Two year': 0}

@app.get("/health")
def health():
    return {"status": "✅ OK"}

@app.get("/")
def root():
    return {
        "message": "Churn Predictor API",
        "version": "1.0.0"
    }

@app.post("/predict")
def predict(request: ChurnPredictionRequest):
    try:
        customer_dict = defaults.copy()
        
        customer_dict['tenure'] = request.tenure
        customer_dict['MonthlyCharges'] = request.monthly_charges
        customer_dict['TotalCharges'] = request.total_charges
        customer_dict['Partner'] = convert_yes_no(request.has_partner)
        customer_dict['Dependents'] = convert_yes_no(request.has_dependents)
        
        customer_dict.update(get_internet_features(request.internet_type))
        customer_dict.update(get_contract_features(request.contract_type))

        X = pd.DataFrame([customer_dict], columns=feature_names)
        X_scaled = scaler.transform(X)
        
        prediction = model.predict(X_scaled)[0]
        probabilities = model.predict_proba(X_scaled)[0]
        churn_prob = probabilities[1]
        
        if churn_prob >= 0.7:
            risk = "HIGH"
        elif churn_prob >= 0.4:
            risk = "MEDIUM"
        else:
            risk = "LOW"
        
        return {
            "churn_probability": round(churn_prob * 100, 2),
            "risk_level": risk,
            "prediction": "CHURN" if prediction == 1 else "RETAIN",
            "confidence": round(max(probabilities) * 100, 2)
        }
    
    except Exception as e:
        return {
            "error": str(e),
            "status": "Failed"
        }