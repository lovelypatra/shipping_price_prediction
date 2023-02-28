import os,sys
from shipment.exception import ShipmentException
from shipment.logger import logging
from datetime import datetime

FILE_NAME = "shipment.csv"
TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"
TRANSFORMER_OBJECT_FILE_NAME = "transformer.pkl"
TARGET_ENCODER_OBJECT_FILE_NAME = "target_encoder.pkl"
MODEL_FILE_NAME = "model.pkl"

class TrainingPipelineConfig:

    def __init__(self):
        try:
            self.artifact_dir = os.path.join(os.getcwd(),"artifact",f"{datetime.now().strftime('%m%d%Y__%H%M%S')}") #artifact directory ....here we are going to generate our output
        except Exception  as e:
            raise ShipmentException(e,sys)     

class DataIngestionConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:
            self.database_name="shipping"
            self.collection_name="shipment"
            self.data_ingestion_dir = os.path.join(training_pipeline_config.artifact_dir , "data_ingestion") 
            self.feature_store_file_path = os.path.join(self.data_ingestion_dir,"feature_store",FILE_NAME)
            self.train_file_path = os.path.join(self.data_ingestion_dir,"dataset",TRAIN_FILE_NAME)
            self.test_file_path = os.path.join(self.data_ingestion_dir,"dataset",TEST_FILE_NAME)
            self.test_size = 0.15
        except Exception  as e:
            raise ShipmentException(e,sys)  
               
    # to return these details in a dictionary        
    def to_dict(self,)->dict:
        try:
            return self.__dict__
        except Exception  as e:
            raise ShipmentException(e,sys)     


class DataValidationConfig:
   def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_validation_dir = os.path.join(training_pipeline_config.artifact_dir , "data_validation")
        self.report_file_path=os.path.join(self.data_validation_dir, "report.yaml")
        self.base_file_path = os.path.join("shipment_price_prediction_dataset.csv")