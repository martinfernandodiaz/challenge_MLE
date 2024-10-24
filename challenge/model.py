import pandas as pd
from sklearn.linear_model import LogisticRegression

from typing import Tuple, Union, List

import pickle

from src.model.constants.features import CATEGORICAL, DATES, TOP
from src.model.constants.values import DATA_DICTIONARY
from src.model.constants.rules import TRESHOLD_IN_MINUTES

#to testing
#from challenge.src.model.constants.features import CATEGORICAL, DATES, TOP
#from challenge.src.model.constants.values import DATA_DICTIONARY
#from challenge.src.model.constants.rules import TRESHOLD_IN_MINUTES

from src.model.functions.transformations import get_delay_feature, get_dummies_features
from src.model.functions.validations import check_missing_features, check_features_for_nan, check_datetime_format, check_values

#to testing
#from challenge.src.model.functions.transformations import get_delay_feature, get_dummies_features
#from challenge.src.model.functions.validations import check_missing_features, check_features_for_nan, check_datetime_format, check_values

import os 

base_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(base_dir)

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
            #basic checks
            check_missing_features(data, CATEGORICAL)
            check_features_for_nan(data, CATEGORICAL)

            for category in CATEGORICAL:
                check_values(data, category, DATA_DICTIONARY[category])

            #dummies generation
            dummies = get_dummies_features(data, CATEGORICAL)

            if target_column:
                #if target, basic checks over needed features
                check_missing_features(data, DATES)
                check_datetime_format(data, DATES, datetime_format="%Y-%m-%d %H:%M:%S")

                target = get_delay_feature(data, TRESHOLD_IN_MINUTES)
                return (dummies[TOP], target)
            else:
                #if no target
                dummies_columns = dummies.columns

                #detecting which created dummies are in the top dummies
                avaible_top_dummies_columns = list(set(dummies_columns).intersection(set(TOP)))
                
                #if created dummies are not equal to top dummies, the remaining ones are created
                if avaible_top_dummies_columns != TOP:
                    to_false_columns = list(set(TOP) - set(avaible_top_dummies_columns))
                    dummies[to_false_columns] = False

                return (dummies[TOP])

        except (KeyError, ValueError) as e:
            return f"Error: {e}" #handler
        

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
        try:
            #basic checks
            check_missing_features(features, TOP)
            check_features_for_nan(features, TOP)
            check_features_for_nan(target, ['delay'])

            n_y0 = len(target[target['delay'] == 0])
            n_y1 = len(target[target['delay'] == 1])
            
            self._model = LogisticRegression(class_weight={1: n_y0/len(target['delay']), 0: n_y1/len(target['delay'])})
            self._model.fit(features, target['delay'])
        
            #model serialization
            with open('./src/model/registry/model.pkl', 'wb') as file:
                pickle.dump(self._model, file)

        except (KeyError, ValueError) as e:
            return f"Error: {e}" #handler
        

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
        try:
            
            if self._model == None:
                # If not model. Load if exists
                with open('./src/model/registry/model.pkl', 'rb') as file:
                    self._model = pickle.load(file)
            
            pred_target = self._model.predict(features)
            pred_target = [int(x) for x in pred_target]

            return pred_target
 
        except FileNotFoundError as e:
            return f"Error: {e}" #handler
