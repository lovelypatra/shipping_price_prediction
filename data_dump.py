import pymongo
import pandas as pd
import json
import os
from shipment.config import mongo_client



DATA_FILE_PATH = "/config/workspace/SCMS_Delivery_History_Dataset.csv"
DATABASE_NAME="shipping"
COLLECTION_NAME="shipment"


if __name__=="__main__":
    df = pd.read_csv(DATA_FILE_PATH)
    print(f"Rows and Columns: {df.shape}")

    #convert dataframe to json format so that we can dump these record in mongo DB
    df.reset_index(drop=True,inplace=True)

    json_record = list(json.loads(df.T.to_json()).values())#json.loads is used to convert any python object
    print(json_record[0])

    #insert converted json record to mongo DB
    mongo_client[DATABASE_NAME][COLLECTION_NAME].insert_many(json_record)