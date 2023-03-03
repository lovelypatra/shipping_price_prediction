import pymongo
from shipment.exception import ShipmentException
from shipment.pipeline.batch_prediction import start_batch_prediction
import os,sys


file_path="/config/workspace/SCMS_Delivery_History_Dataset.csv"

if __name__=="__main__":
     try:  
          output_file = start_batch_prediction(input_file_path=file_path)
          print(output_file)


     except Exception as e:
          raise ShipmentException(e, sys)

          