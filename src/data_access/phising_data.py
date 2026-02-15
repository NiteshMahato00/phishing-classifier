import sys
from typing import List

# from import mongo_operation as mongo
# from pymongo import MongoClient
import numpy as np
import pandas as pd
from src.constant import *
from pymongo import MongoClient
from src.exception import CustomException
import os


class PhisingData:
    """
    This class help to export entire mongo db record as pandas dataframe
    """

    def __init__(self,
                 database_name: str):
        """
        """
        try:

            self.database_name = database_name
            self.mongo_url = os.getenv("MONGO_DB_URL")

        except Exception as e:
            raise CustomException(e, sys)

    def get_collection_names(self) -> List:

        mongo_db_client = MongoClient(self.mongo_url)
        collection_names = mongo_db_client[self.database_name].list_collection_names()
        return collection_names

    def get_collection_data(self, collection_name: str) -> pd.DataFrame:

        client = MongoClient(self.mongo_url)
        db = client[self.database_name]
        collection = db[collection_name]

        data = list(collection.find())
        df = pd.DataFrame(data)

        if "_id" in df.columns:
            df = df.drop(columns=["_id"])

        df = df.replace({"na": np.nan})
        return df

    def export_collections_as_dataframe(
            self) -> pd.DataFrame:
        try:
            """
            export entire collectin as dataframe:
            return dd.DataFrame of collection
            """

            collections = self.get_collection_names()

            for collection_name in collections:
                df = self.get_collection_data(collection_name=collection_name)
                yield collection_name, df



        except Exception as e:
            raise CustomException(e, sys)
