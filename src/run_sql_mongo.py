import os
import sys
from random import randint

import pymongo
from dotenv import load_dotenv


load_dotenv()
CONNECTION_STRING = os.environ.get("COSMOS_CONNECTION_STRING")
DB_NAME = "adventureworks"
COLLECTION_NAME = "products"


def initiate_cosmos_db(client):
    """ Initiate mongo db/collection/document"""

    # Create database if it doesn't exist
    db = client[DB_NAME]
    if DB_NAME not in client.list_database_names():
        # Create a database with 400 RU throughput that can be shared across
        # the DB's collections
        db.command({"customAction": "CreateDatabase", "offerThroughput": 400})
        print("Created db '{}' with shared throughput.\n".format(DB_NAME))
    else:
        print("Using database: '{}'.\n".format(DB_NAME))

    # Create collection if it doesn't exist
    collection = db[COLLECTION_NAME]
    if COLLECTION_NAME not in db.list_collection_names():
        # Creates a unsharded collection that uses the DBs shared throughput
        db.command(
            {"customAction": "CreateCollection", "collection": COLLECTION_NAME}
        )
        print("Created collection '{}'.\n".format(COLLECTION_NAME))
    else:
        print("Using collection: '{}'.\n".format(COLLECTION_NAME))

    indexes = [
        {"key": {"_id": 1}, "name": "_id_1"},
        {"key": {"name": 2}, "name": "_id_2"},
    ]
    db.command(
        {
            "customAction": "UpdateCollection",
            "collection": COLLECTION_NAME,
            "indexes": indexes,
        }
    )
    print("Indexes are: {}\n".format(sorted(collection.index_information())))

    """Create new document and upsert (create or replace) to collection"""
    product = {
        "category": "gear-surf-surfboards",
        "name": "Yamba Surfboard-{}".format(randint(50, 5000)),
        "quantity": 1,
        "sale": False,
    }
    result = collection.update_one(
        {"name": product["name"]}, {"$set": product}, upsert=True
    )
    print("Upserted document with _id {}\n".format(result.upserted_id))

    return collection, result


def main():

    # initiate an example collection
    client = pymongo.MongoClient(CONNECTION_STRING)
    collection, result = initiate_cosmos_db(client)

    print("\n###########################################################")

    # Use the find_one method to get a document.
    doc = collection.find_one({"_id": result.upserted_id})
    print("Found a document with _id {}: {}\n".format(result.upserted_id, doc))

    # Query for documents in the collection
    print("Products with category 'gear-surf-surfboards':\n")
    allProductsQuery = {"category": "gear-surf-surfboards"}
    for doc in collection.find(allProductsQuery).sort(
        "name", pymongo.ASCENDING
    ):
        print("Found a product with _id {}: {}\n".format(doc["_id"], doc))


if __name__ == "__main__":
    main()
