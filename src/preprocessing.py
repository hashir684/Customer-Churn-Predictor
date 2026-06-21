import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

def get_engine():
    url = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(url)
    return engine

def load_data():
    engine = get_engine()
    query = "SELECT * FROM customers"
    df = pd.read_sql(query, engine)
    return df

def check_missing_values(df):
    print("\nCHECKING MISSING VALUES : \n")
    
    missing = df.isnull().sum()
    if missing.sum() == 0:
        print("No missing values found!")
    else:
        print("\nMissing values found :")
        print(missing[missing > 0])
    
    return df

def fix_data_types(df):
    print("\nFIXING DATA TYPES & BINARY ENCODING : ")
    if df['TotalCharges'].dtype == 'object':   #charges conversion to float if in string
        df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')

    print("\nBinary Encoding :")
    temp_df = df.select_dtypes(include=['object']).columns
    for col in temp_df:
        if set(df[col].unique()).issubset({'Yes', 'No'}):
            df[col] = df[col].map({'Yes': 1, 'No': 0})
            print(f"{col}")
    return df

def one_hot_encode(df):
    print("\nONE-HOT ENCODING :\n")
    categorical_cols = [col for col in df.select_dtypes(include=['object']).columns if col not in ['customerID']]

    if categorical_cols:
        original_cols = len(df.columns)  
        
        print(f"Encoding: {categorical_cols}")
        df = pd.get_dummies(df, columns=categorical_cols, drop_first=True)
        
        new_cols = len(df.columns) - original_cols 
        print(f"   Original columns : {original_cols}")
        print(f"   New columns: {len(df.columns)}")
        print(f"   Added: {new_cols}")
    
    return df

def remove_duplicates(df):
    print("\nREMOVING DUPLICATES :\n")
    initial_rows = len(df)
    df = df.drop_duplicates()
    removed = initial_rows - len(df)
    
    if removed == 0:
        print("No duplicates found!")
    else:
        print(f"Removed {removed} duplicate rows")
    return df

def handle_outliers(df):
    print("\nHANDLING OUTLIERS :\n")
    numerical_cols = df.select_dtypes(include=[np.number]).columns
    
    for col in numerical_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1        
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers = ((df[col] < lower_bound) | (df[col] > upper_bound)).sum()
        
        if outliers > 0:
            print(f"{col}: Found {outliers} outliers")
            print(f"Range: {lower_bound:.2f} - {upper_bound:.2f}")
        else:
            print(f"{col}: No outliers")
    
    return df

def clean_data():
    print("STARTING DATA CLEANING PIPELINE...\n")
    df = load_data()
    print(f"Loaded {len(df)} rows from MySQL")
    print(f"Columns: {len(df.columns)}")
    
    df = check_missing_values(df)
    df = fix_data_types(df)
    df = remove_duplicates(df)
    df = one_hot_encode(df)
    df = handle_outliers(df)
    
    print(f"\nCLEANING COMPLETE!")
    print(f"Final dataset: {len(df)} rows, {len(df.columns)} columns")
    return df

def save_cleaned_data(df):
    print("\nSAVING CLEANED DATA : \n")
    engine = get_engine()
    
    try:
        df.to_sql(
            "customers_clean",
            con=engine,
            if_exists="replace",
            index=False
        )
        print("\nCleaned data saved to 'customers_clean' table!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    df_clean = clean_data()
    save_cleaned_data(df_clean)
    print("Clean Data Saved!")
 