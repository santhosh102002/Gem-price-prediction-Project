import os
import sys
from src.logger import logging
from src.exception import CustomException
import pandas as pd

from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransforamtion
from src.components.model_trainer import ModelTrainer

if __name__ == '__main__':
    obj = DataIngestion()
    train_data,test_data = obj.initiate_data_ingestion()
    print(train_data,test_data)
    data_transforamtion = DataTransforamtion()
    train_array,test_array,obj_path = data_transforamtion.initiate_data_transformation(train_data,test_data)
    model_obj = ModelTrainer()
    model_obj.initiate_model_training(train_array=train_array,test_array=test_array)
    


    