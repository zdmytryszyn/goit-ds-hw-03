import json


from pymongo import MongoClient
from pymongo.server_api import ServerApi

client = MongoClient(
    "mongodb+srv://zoreslavd:113522Aa@mycluster.bnmc1.mongodb.net/?retryWrites=true&w=majority&appName=MyCluster",
    server_api=ServerApi('1')
)

db = client.goit_hw_03

if __name__ == "__main__":
    with open('quotes.json', 'r', encoding='utf-8') as q:
        quotes = json.load(q)

    with open('authors.json', 'r', encoding='utf-8') as a:
        authors = json.load(a)

    if db.quotes.count_documents({}) > 0:
        db.quotes.delete_many({})
    if db.authors.count_documents({}) > 0:
        db.authors.delete_many({})

    try:
        db.quotes.insert_many(quotes)
        db.authors.insert_many(authors)
    except Exception as e:
        print(e)
