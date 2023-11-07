from pymongo import MongoClient
import pandas as pd
import time
import json

client = MongoClient("localhost:27017")
client.list_database_names()
db = client["ironhack"]
c = db.get_collection("companies")

def counting_companies_in_a_category(category):
    query = {"category_code": category}
    projection = {"_id":0, "name":1,"category_code":1, "offices":1}
    total = len(list(c.find(query, projection)))
    print(f'Total number companies of {category} is {total}')


# Creating a function to filter just the companies that have at least 1 M of money raised and less than 100 employees
def create_df_filtered_companies_and_export():
    pipeline = [
        {"$match": {
                "total_money_raised": {
                    "$regex": r"\d+\.\d+M"
                }}},
        {"$match": {
                "number_of_employees": {
                    "$lte": 100
                }}},
        {"$project": {
                "_id": 0,
                "name": 1,
                "total_money_raised": 1,
                "category_code":1,
                "number_of_employees": 1,
                "offices.city":1,
                "offices.latitude": 1,
                "offices.longitude": 1,
            }},
        {"$sort": {
                "number_of_employees": -1  # 1 for ascending order, -1 for descending
            }},
    ]
    results = list(c.aggregate(pipeline))
    df = pd.DataFrame(results)
    # as the result df in the column offices is a list: '[{'city': 'Longmont', 'latitude': 40.146898, '...' need to transform
    location_df = pd.json_normalize(results, record_path=['offices'], 
                                    meta=['name'], 
                                    errors='ignore')
    [['name', 'city', 'latitude', 'longitude']]
    # merging the two data frames
    merged_df = pd.merge(location_df, df, on='name')
    # getting just the column that is needed and droping columns that have null values 
    merged_df = merged_df[["name", "city", "category_code", "number_of_employees","total_money_raised", "latitude", "longitude"]]
    merged_df.dropna(inplace=True)
    # downloading the subset as a jason
    merged_df.to_csv("data/filter_companies.csv", index=False)
    print("exported")
