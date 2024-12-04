import pymysql
from pymongo import MongoClient
from transformers import AutoTokenizer
from datetime import datetime

def connect_to_mysql(host, port, user, password, database):
    """
    Connects to the MySQL database.
    """
    connection = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database
    )
    print("MySQL connection established.")
    return connection

def fetch_data_from_mysql(connection):
    """
    Fetches data from MySQL.
    """
    query = "SELECT id, content FROM texts;"
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute(query)
        results = cursor.fetchall()
    print(f"{len(results)} rows retrieved from MySQL.")
    return results

def connect_to_mongodb(host, port, database):
    """
    Connects to MongoDB.
    """
    client = MongoClient(host, port)
    db = client[database]
    print("MongoDB connection established.")
    return db

def tokenize_texts(data, tokenizer_name):
    """
    Tokenizes texts using a pre-trained tokenizer.
    """
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
    tokenized_data = []

    for record in data:
        tokens = tokenizer.encode(record['content'], truncation=True, max_length=512)
        tokenized_data.append({
            "id": record['id'],
            "text": record['content'],
            "tokens": tokens,
            "metadata": {
                "source": "mysql",
                "processed_at": datetime.utcnow().isoformat() + "Z"
            }
        })
    print(f"{len(tokenized_data)} texts tokenized.")
    return tokenized_data

def insert_into_mongodb(collection, data):
    """
    Inserts data into MongoDB.
    """
    result = collection.insert_many(data)
    print(f"{len(result.inserted_ids)} documents inserted into MongoDB.")

def fetch_sample_from_mongodb(collection, sample_size=5):
    """
    Fetches a sample of documents from MongoDB.
    """
    sample = list(collection.find().limit(sample_size))
    print(f"Sample data from MongoDB ({sample_size} documents):")
    for doc in sample:
        print(doc)
    return sample

def main():
    # Connect to MySQL
    mysql_connection = connect_to_mysql(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="root",
        database="staging"
    )

    # Fetch data
    data = fetch_data_from_mysql(mysql_connection)

    # Close MySQL connection
    mysql_connection.close()

    # Tokenize texts
    tokenized_data = tokenize_texts(data, tokenizer_name="distilbert-base-uncased")

    # Connect to MongoDB
    mongodb = connect_to_mongodb(
        host="127.0.0.1",
        port=27017,
        database="curated"
    )

    # Insert into MongoDB
    collection = mongodb["wikitext"]
    insert_into_mongodb(collection, tokenized_data)
    
    # Fetch a sample of data from MongoDB
    fetch_sample_from_mongodb(collection, sample_size=5)

if __name__ == "__main__":
    main()
