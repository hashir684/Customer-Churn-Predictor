import pandas as pd
import numpy as np
import joblib
import os
import warnings
warnings.filterwarnings('ignore')

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix, roc_curve, auc)
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

from db import get_engine
from feature_eng import load_clean_data, separate_features_target

def load_prepared_data():
    print("LOADING PREPARED DATA :")
    df = load_clean_data()
    df = df.drop(columns=['customerID'])
    X, y = separate_features_target(df)
    
    print(f"\nChecking for NaN values...")
    nan_count = X.isnull().sum().sum()
    print(f"   NaN values found: {nan_count}")
    
    if nan_count > 0:
        print(f"   Dropping rows with NaN...")
        X = X.dropna()
        y = y[X.index]  
        print(f"   After dropping NaN: {X.shape[0]} rows")
    
    scaler = joblib.load('models/scaler.pkl')
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    X_train_scaled = scaler.transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    X_train_scaled = pd.DataFrame(X_train_scaled, columns=X.columns, index=X_train.index)
    X_test_scaled = pd.DataFrame(X_test_scaled, columns=X.columns, index=X_test.index)
    
    print(f"\nChecking for NaN after scaling...")
    nan_train = X_train_scaled.isnull().sum().sum()
    nan_test = X_test_scaled.isnull().sum().sum()
    print(f"   NaN in train: {nan_train}")
    print(f"   NaN in test: {nan_test}")
    
    if nan_train > 0 or nan_test > 0:
        print(f"   WARNING: NaN found after scaling!")
        print(f"   Filling NaN with 0...")
        X_train_scaled = X_train_scaled.fillna(0)
        X_test_scaled = X_test_scaled.fillna(0)
    
    print(f"\nData ready!")
    print(f"X_train shape: {X_train_scaled.shape}")
    print(f"X_test shape: {X_test_scaled.shape}")
    return X_train_scaled, X_test_scaled, y_train, y_test

def train_logistic_regression(X_train, y_train):
    print("TRAINING LOGISTIC REGRESSION : ")
    model = LogisticRegression(max_iter=1000, random_state=42)
    model.fit(X_train, y_train)
    print("Logistic Regression trained!")
    return model

def train_random_forest(X_train, y_train):
    print("TRAINING RANDOM FOREST : ")
    model = RandomForestClassifier(n_estimators=100,random_state=42,n_jobs=-1)
    model.fit(X_train, y_train)
    
    print("Random Forest trained!")
    return model

def train_xgboost(X_train, y_train):
    print("TRAINING XGBOOST : ") 
    model = XGBClassifier(n_estimators=100,random_state=42,use_label_encoder=False,eval_metric='logloss',verbosity=0)
    model.fit(X_train, y_train)
    print("XGBoost trained!")
    return model

def evaluate_model(model, X_test, y_test, model_name):
    print(f"EVALUATING {model_name.upper()} : ")
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_pred_proba)
    
    print(f"\n{model_name} Metrics:")
    print(f"   Accuracy:  {accuracy:.4f}")
    print(f"   Precision: {precision:.4f}")
    print(f"   Recall:    {recall:.4f}")
    print(f"   F1-Score:  {f1:.4f}")
    print(f"   ROC-AUC:   {roc_auc:.4f}")
    
    return {
        'Model': model_name,
        'Accuracy': accuracy,
        'Precision': precision,
        'Recall': recall,
        'F1-Score': f1,
        'ROC-AUC': roc_auc
    }

def compare_models(results):
    print("MODEL COMPARISON : ")
    results_df = pd.DataFrame(results)
    print("\n" + results_df.to_string(index=False))
    
    best_idx = results_df['F1-Score'].idxmax()
    best_model = results_df.loc[best_idx, 'Model']
    print(f"\n Best Model: {best_model}")
    print(f"   F1-Score: {results_df.loc[best_idx, 'F1-Score']:.4f}")
    return best_model

def save_best_model(model, model_name):
    print("SAVING BEST MODEL : ")
    os.makedirs('models', exist_ok=True)
    joblib.dump(model, 'models/churn_model.pkl')
    
    print(f"\n Model saved successfully!")
    print(f"   Model: {model_name}")
    print(f"   Location: models/churn_model.pkl")

if __name__ == "__main__":
    print("MODEL TRAINING PIPELINE : ")
    X_train, X_test, y_train, y_test = load_prepared_data()
    print("TRAINING ALL MODELS : ")
    
    lr_model = train_logistic_regression(X_train, y_train)
    rf_model = train_random_forest(X_train, y_train)
    xgb_model = train_xgboost(X_train, y_train)
    
    print("EVALUATING ALL MODELS : ")
    results = []
    results.append(evaluate_model(lr_model, X_test, y_test, "Logistic Regression"))
    results.append(evaluate_model(rf_model, X_test, y_test, "Random Forest"))
    results.append(evaluate_model(xgb_model, X_test, y_test, "XGBoost"))

    best_model_name = compare_models(results)
    
    if best_model_name == "Logistic Regression":
        best_model = lr_model
    elif best_model_name == "Random Forest":
        best_model = rf_model
    else:
        best_model = xgb_model    
    save_best_model(best_model, best_model_name)
    
    print("\nMODEL TRAINING COMPLETE!")
