import pandas as pd

def check_missing_features(df, features):
    missing_features = [feature for feature in features if feature not in df.columns]
    
    if missing_features:
        raise ValueError(f"The following features are missing from the DataFrame: {missing_features}")

def check_features_for_nan(df, features):
    nan_features = [feature for feature in features if df[feature].isna().any()]  
    
    if nan_features:
        raise ValueError(f"The following features contain NaN values: {nan_features}")
    
def check_datetime_format(df, features, datetime_format="%Y-%m-%d %H:%M:%S"):
    datetime_features = [pd.to_datetime(df[feature], format=datetime_format, errors='raise') for feature in features]  

    for datetime_feature in datetime_features:
        if datetime_feature.isna().any():
            raise ValueError("Incorrect data format, should be YYYY-MM-DD HH:MM:SS")
        
def check_values(df, feature, values):
    all_in_features = df[feature].isin(values).all()
    
    if not all_in_features:
        raise ValueError(f"Values in feature {feature} not allowed")



