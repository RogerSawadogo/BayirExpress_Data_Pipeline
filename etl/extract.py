from pymongo import MongoClient
import pandas as pd
from etl.config import MONGO_URI, MONGO_DB_NAME

def extract_collection(collection_name: str) -> pd.DataFrame:
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB_NAME]
    collection = db[collection_name]

    data = list(collection.find())
    df = pd.DataFrame(data)

    client.close()
    return df
