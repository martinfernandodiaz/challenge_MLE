import pandas as pd
from sklearn.linear_model import LogisticRegression

from typing import Tuple, Union, List

from challenge.src.model_modules.transformations import get_delay_feature, get_dummies_features
from challenge.src.model_modules.validations import check_missing_features, check_features_for_nan, check_datetime_format

class DelayModel:

    def __init__(
        self
    ):
        self._model = None # Model should be saved in this attribute.

    def preprocess(
            self,
            data: pd.DataFrame,
            target_column: str = None
        ) -> Union[Tuple[pd.DataFrame, pd.DataFrame], pd.DataFrame]:
        """
        Prepare raw data for training or predict.

        Args:
            data (pd.DataFrame): raw data.
            target_column (str, optional): if set, the target is returned.

        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]: features and target.
            or
            pd.DataFrame: features.
        """
        try:
            #bussiness rule
            threshold_in_minutes = 15

            #variables needed to preprocess raw data
            categorical_features = ['OPERA', 'TIPOVUELO', 'MES'] 
            dates_features = ['Fecha-O', 'Fecha-I']
            
            #selected top features
            top_10_features = [
                            "OPERA_Latin American Wings", 
                            "MES_7",
                            "MES_10",
                            "OPERA_Grupo LATAM",
                            "MES_12",
                            "TIPOVUELO_I",
                            "MES_4",
                            "MES_11",
                            "OPERA_Sky Airline",
                            "OPERA_Copa Air"
                        ]
            
            #basic checks
            check_missing_features(data, categorical_features + dates_features)
            check_datetime_format(data, dates_features, datetime_format="%Y-%m-%d %H:%M:%S")
            check_features_for_nan(data, categorical_features)

            #dummies generation
            dummies = get_dummies_features(data, categorical_features)

            if target_column:
                target = get_delay_feature(data, threshold_in_minutes)
                return (dummies[top_10_features], target)
            
            return(dummies[top_10_features])

        except (KeyError, ValueError) as e:
            print(f"Error: {e}")
        
        return

    def fit(
        self,
        features: pd.DataFrame,
        target: pd.DataFrame
    ) -> None:
        """
        Fit model with preprocessed data.

        Args:
            features (pd.DataFrame): preprocessed data.
            target (pd.DataFrame): target.
        """
        
        n_y0 = len(target[target['delay'] == 0])
        n_y1 = len(target[target['delay'] == 1])
        
        self._model = LogisticRegression(class_weight={1: n_y0/len(target['delay']), 0: n_y1/len(target['delay'])})
        self._model.fit(features, target['delay'])
        
        return

    def predict(
        self,
        features: pd.DataFrame
    ) -> List[int]:
        """
        Predict delays for new flights.

        Args:
            features (pd.DataFrame): preprocessed data.
        
        Returns:
            (List[int]): predicted targets.
        """
        pred_target = self._model.predict(features)
        pred_target = [int(x) for x in pred_target]
        
        return pred_target
    
