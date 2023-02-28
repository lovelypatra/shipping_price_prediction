from shipment.entity import artifact_entity,config_entity
from shipment.exception import ShipmentException
from shipment.logger import logging
from scipy.stats import ks_2samp
from typing import Optional
import os,sys 
import pandas as pd
from shipment import utils
import numpy as np
from shipment.config import TARGET_COLUMN
from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection
import json


class DataValidation:
    
    def __init__(self,
                    data_validation_config:config_entity.DataValidationConfig,
                    data_ingestion_artifact:artifact_entity.DataIngestionArtifact):
        try:
            logging.info(f"{'>>'*20} Data Validation {'<<'*20}")
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact=data_ingestion_artifact
            self.validation_error=dict()
        except Exception as e:
            raise ShipmentException(e, sys)

    def drop_unwanted_columns(self,df:pd.DataFrame)->pd.DataFrame:
        '''
        This function will drop the unnecessary columns in dataset
        Params:
        df: Accepts a pandas dataframe
        =================================================
        returns Pandas DataFrame
        '''
        try:            
            #drop unnecessary columns as they are not required for model training
            columns_to_drop:list =  ['ID', 'Project Code', 'PQ #', 'PO / SO #', 'ASN/DN #','Item Description','PQ First Sent to Client Date',
            'PO Sent to Vendor Date','Scheduled Delivery Date','Delivered to Client Date','Delivery Recorded Date']

            df = df.drop(columns_to_drop,axis =1)
            
            return df

            
        except Exception as e:
                raise ShipmentException(e,sys)

    def data_drift(self,base_df:pd.DataFrame,current_df:pd.DataFrame,report_key_name:str):
        try:
            profile = Profile(sections=[DataDriftProfileSection()])
            profile.calculate(base_df, current_df)
            drift_report = json.loads(profile.json())

            self.validation_error[report_key_name]=drift_report
        except Exception as e:
            raise ShipmentException(e, sys)

    def initiate_data_validation(self)->artifact_entity.DataValidationArtifact:
        try:
            logging.info(f"Reading base dataframe")
            base_df = pd.read_csv(self.data_validation_config.base_file_path)
            
            logging.info(f"Dropping unwanted columns")
            base_df=self.drop_unwanted_columns(df=base_df)

            logging.info(f"Reading train dataframe")
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            logging.info(f"Reading test dataframe")
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)

            logging.info(f"Dropping unwanted columns from train df")
            train_df = self.drop_unwanted_columns(df=train_df)
            logging.info(f"Dropping unwanted columns from test df")
            test_df = self.drop_unwanted_columns(df=test_df)

            logging.info(f"detecting data drift in train df")
            self.data_drift(base_df=base_df, current_df=train_df,report_key_name="data_drift_within_train_dataset")
            
            logging.info(f"detecting data drift in test df")
            self.data_drift(base_df=base_df, current_df=test_df,report_key_name="data_drift_within_test_dataset")

            #write the report
            logging.info("Writing report in yaml file")
            utils.write_yaml_file(file_path=self.data_validation_config.report_file_path,
            data=self.validation_error)

            data_validation_artifact = artifact_entity.DataValidationArtifact(report_file_path=self.data_validation_config.report_file_path,)
            logging.info(f"Data validation artifact: {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise ShipmentException(e, sys)