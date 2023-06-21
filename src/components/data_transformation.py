from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
import numpy as np
import pandas as pd

from src.exception import CustomException
from src.logger import logging
import sys
import os
from dataclasses import dataclass
from src.components.data_ingestion import DataIngestion
from src.utils import save_object
@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts','preprocessor.pkl')

class DataTransforamtion:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()
    def get_data_transformation(self):
        try:
            logging.info('Data Transforamtion is initiated')
            # cat and numerical colmns
            categorical_cols = ['cut','color','clarity']
            numerical_cols = ['carat','depth','table','x','y','z']
            # Define the custom ranking for each ordinal variable
            cut_categories = ['Fair', 'Good', 'Very Good','Premium','Ideal']
            color_categories = ['D', 'E', 'F', 'G', 'H', 'I', 'J']
            clarity_categories = ['I1','SI2','SI1','VS2','VS1','VVS2','VVS1','IF']

            logging.info('Data Transforamtion pipeline Initiated')

            numerical_pipeline = Pipeline(
                steps=[
                    ('imputer',SimpleImputer(strategy='median')),
                    ('scaler',StandardScaler())
                ]
            )
            categorical_pipeline = Pipeline(
                steps=[
                    ('imputer',SimpleImputer(strategy='most_frequent')),
                    ('ordinalencoder',OrdinalEncoder(categories=[cut_categories,color_categories,clarity_categories])),
                    ('scaler',StandardScaler())
                ]
            )
            preprocessor = ColumnTransformer(
                [
                    ('numerical_pipeline',numerical_pipeline,numerical_cols),
                    ('categorical_pipeline',categorical_pipeline,categorical_cols)
                ]
            )

            logging.info('Data Tranforamtion is completed')

            return preprocessor
                    
        except Exception as e:
            logging.info('Exception occured in Data Transforamtion')
            raise CustomException(e,sys)
    def initiate_data_transformation(self,train_data_path,test_data_path):
           try:
            #    self.train_data_path,self.test_data_path = DataIngestion().initiate_data_ingestion()
               train_df = pd.read_csv(train_data_path)
               test_df = pd.read_csv(test_data_path)

               preprocessing_obj = self.get_data_transformation()

               target_columns = 'price'
               drop_columns = [target_columns,'id']
               
               input_feature_train_df = train_df.drop(columns=drop_columns,axis=1)
               target_feature_train_df = train_df[target_columns]
               input_feature_test_df = test_df.drop(columns=drop_columns,axis=1)
               target_feature_test_df = test_df[target_columns]

               input_feature_train_df_arr = preprocessing_obj.fit_transform(input_feature_train_df)
               input_feature_test_df_arr = preprocessing_obj.transform(input_feature_test_df)

               train_array = np.c_[input_feature_train_df_arr,np.array(target_feature_train_df)]
               test_array = np.c_[input_feature_test_df_arr,np.array(target_feature_test_df)]

               save_object(self.data_transformation_config.preprocessor_obj_file_path,obj=preprocessing_obj)

               return(
                   train_array,
                   test_array,
                   self.data_transformation_config.preprocessor_obj_file_path
               )





               


           except Exception as e:
            logging.info('Exception occured in Data Transforamtion')
            raise CustomException(e,sys)
