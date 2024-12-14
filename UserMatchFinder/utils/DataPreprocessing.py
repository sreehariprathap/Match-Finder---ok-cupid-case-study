import pandas as pd
from sklearn.preprocessing import OneHotEncoder, LabelEncoder, StandardScaler

# Data preprocessing
def preprocess_data(df):
    # Standardize categorical fields using one-hot encoding
    categorical_fields = ['status', 'sex', 'orientation']
    df = pd.get_dummies(df, columns=categorical_fields)
    
    # Label encode other categorical fields if necessary
    label_encoder = LabelEncoder()
    for column in df.select_dtypes(include=['object']).columns:
        df[column] = label_encoder.fit_transform(df[column])
    
    # Normalize numerical fields
    numerical_fields = ['height', 'income']
    scaler = StandardScaler()
    df[numerical_fields] = scaler.fit_transform(df[numerical_fields])
    
    return df