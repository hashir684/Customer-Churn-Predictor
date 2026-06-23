import os
import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from db import get_engine

def load_clean_data():
    """Load cleaned data from MySQL"""
    engine = get_engine()
    query = "SELECT * FROM customers_clean"
    df = pd.read_sql(query, engine)

    print(f"\nLoaded {len(df)} records")
    print(f"Dataset Shape: {df.shape}")
    return df

def separate_features_target(df):
    y = df["Churn"]
    X = df.drop(columns=["Churn"])
    print("\nFeature/Target Separation")
    print(f"Features Shape: {X.shape}")
    print(f"Target Shape: {y.shape}")

    print("\nChurn Distribution:")
    print(y.value_counts())
    return X, y


def split_data(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.20,random_state=42,stratify=y)
        
    print("\nTrain/Test Split")
    print(f"X_train: {X_train.shape}")
    print(f"X_test : {X_test.shape}")
    print(f"y_train: {y_train.shape}")
    print(f"y_test : {y_test.shape}")
    return X_train, X_test, y_train, y_test

def scale_features(X_train, X_test):
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    X_train_scaled = pd.DataFrame(X_train_scaled,columns=X_train.columns,index=X_train.index)
    X_test_scaled = pd.DataFrame(X_test_scaled,columns=X_test.columns,index=X_test.index)
    print("\nScaling Complete")
    print(f"Train Min: {X_train_scaled.min().min():.4f}")
    print(f"Train Max: {X_train_scaled.max().max():.4f}")

    return X_train_scaled, X_test_scaled, scaler

def save_scaler(scaler):
    os.makedirs("models", exist_ok=True)
    joblib.dump(scaler,"models/scaler.pkl")
    print("\nScaler saved successfully")
    print("Location: models/scaler.pkl")

if __name__ == "__main__":
    print("FEATURE ENGINEERING PIPELINE :")
    df = load_clean_data()
    df = df.drop(columns=['customerID'])
    non_numeric = df.select_dtypes(include=["object"]).columns.tolist()

    if non_numeric:
        print("\nERROR: Non-numeric columns found:")
        print(non_numeric)
        exit()

    X, y = separate_features_target(df)
    X_train, X_test, y_train, y_test = split_data(X, y)
    X_train_scaled, X_test_scaled, scaler = scale_features(X_train, X_test)
    save_scaler(scaler)

    print("\nFEATURE ENGINEERING COMPLETE!")