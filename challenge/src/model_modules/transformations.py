import pandas as pd
import numpy as np 
from datetime import datetime

def get_min_diff(data):
    fecha_o = datetime.strptime(data['Fecha-O'], '%Y-%m-%d %H:%M:%S')
    fecha_i = datetime.strptime(data['Fecha-I'], '%Y-%m-%d %H:%M:%S')
    min_diff = ((fecha_o - fecha_i).total_seconds())/60
    return min_diff

def get_delay_feature(data, threshold_in_minutes):
    min_diff = data.apply(get_min_diff, axis = 1)
    delay = np.where(min_diff > threshold_in_minutes, 1, 0)
    return pd.DataFrame(delay, columns=['delay']) 

def get_dummies_features(data, categorical_features):
    dummies  = [pd.get_dummies(data[feature], prefix = feature) for feature in categorical_features]
    features = pd.concat(dummies, axis = 1)
    return features
