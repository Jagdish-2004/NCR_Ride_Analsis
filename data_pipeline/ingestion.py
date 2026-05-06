import pandas as pd
import pymongo
import os
import uuid
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "ride_analyzer")

def ingest_data(cleaned_csv_path):
    print("Connecting to MongoDB...")
    client = pymongo.MongoClient(MONGODB_URI)
    db = client[DATABASE_NAME]
    collection = db['rides']

    print(f"Loading cleaned data from {cleaned_csv_path}...")
    df = pd.read_csv(cleaned_csv_path)
    
    # Keep pickup_date and pickup_time as strings
    df = df.where(pd.notnull(df), None)
    records = df.to_dict('records')
    
    if not records:
        print("No records to insert.")
        return

    # Drop existing collection to prevent duplicates on rerun
    collection.drop()

    print(f"Preparing to insert {len(records)} records into MongoDB...")
    # Generate UUIDs for ride_id if not present
    for record in records:
        if 'ride_id' not in record or pd.isna(record['ride_id']):
            record['ride_id'] = str(uuid.uuid4())
    
    # Bulk insert
    try:
        collection.insert_many(records, ordered=False)
        print(f"Successfully inserted {len(records)} records.")
    except pymongo.errors.BulkWriteError as e:
        print(f"Bulk write error occurred (possibly duplicates). Inserted {e.details['nInserted']} records.")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cleaned_file = os.path.join(base_dir, "ncr_ride_bookings_cleaned.csv")
    
    if os.path.exists(cleaned_file):
        ingest_data(cleaned_file)
    else:
        print(f"Cleaned file not found: {cleaned_file}. Please run cleaning.py first.")
