import pymysql
from pymongo import MongoClient
from transformers import AutoTokenizer
from datetime import datetime

def connect_to_mysql(host, port, user, password, database):
    """
    Connecte à la base de données MySQL.
    """
    connection = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database
    )
    print("Connexion MySQL établie.")
    return connection

def fetch_data_from_mysql(connection):
    """
    Récupère les données depuis MySQL.
    """
    query = "SELECT id, content FROM texts;"
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute(query)
        results = cursor.fetchall()
    print(f"{len(results)} lignes récupérées depuis MySQL.")
    return results

def connect_to_mongodb(host, port, database):
    """
    Connecte à MongoDB.
    """
    client = MongoClient(host, port)
    db = client[database]
    print("Connexion MongoDB établie.")
    return db

def tokenize_texts(data, tokenizer_name):
    """
    Tokenise les textes en utilisant un tokenizer pré-entraîné.
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
    print(f"{len(tokenized_data)} textes tokenisés.")
    return tokenized_data

def insert_into_mongodb(collection, data):
    """
    Insère les données dans MongoDB.
    """
    result = collection.insert_many(data)
    print(f"{len(result.inserted_ids)} documents insérés dans MongoDB.")

def fetch_sample_from_mongodb(collection, sample_size=5):
    """
    Récupère un échantillon de documents depuis MongoDB.
    """
    sample = list(collection.find().limit(sample_size))
    print(f"Échantillon de données depuis MongoDB ({sample_size} documents) :")
    for doc in sample:
        print(doc)
    return sample

def main():
    # Connexion à MySQL
    mysql_connection = connect_to_mysql(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="root",
        database="staging"
    )

    # Récupération des données
    data = fetch_data_from_mysql(mysql_connection)

    # Fermeture de la connexion MySQL
    mysql_connection.close()

    # Tokenisation des textes
    tokenized_data = tokenize_texts(data, tokenizer_name="distilbert-base-uncased")

    # Connexion à MongoDB
    mongodb = connect_to_mongodb(
        host="127.0.0.1",
        port=27017,
        database="curated"
    )

    # Insertion dans MongoDB
    collection = mongodb["wikitext"]
    insert_into_mongodb(collection, tokenized_data)
    
    # Récupérer un échantillon de données de MongoDB
    fetch_sample_from_mongodb(collection, sample_size=5)

if __name__ == "__main__":
    main()
