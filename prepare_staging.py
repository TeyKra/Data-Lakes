import os
import pandas as pd
import mysql.connector
from mysql.connector import Error
import boto3
import argparse


def download_from_s3(bucket_name, file_key, download_path, endpoint_url):
    """
    Télécharge un fichier depuis un bucket S3.
    """
    s3 = boto3.client('s3', endpoint_url=endpoint_url)
    s3.download_file(bucket_name, file_key, download_path)
    print(f"Fichier téléchargé depuis S3 : {file_key} -> {download_path}")


def clean_data(file_path):
    """
    Nettoie les données : supprime les doublons et les lignes vides.
    """
    df = pd.read_csv(file_path)
    print("Colonnes disponibles dans le fichier :", df.columns)  # Vérification
    original_count = len(df)
    df.drop_duplicates(inplace=True)
    df.dropna(inplace=True)
    cleaned_count = len(df)
    print(f"Données nettoyées : {original_count - cleaned_count} lignes supprimées.")
    return df



def connect_to_mysql(host, port, user, password, database):
    """
    Établit une connexion à la base MySQL.
    """
    try:
        connection = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        if connection.is_connected():
            print(f"Connexion établie à la base MySQL : {database}")
            return connection
    except Error as e:
        print(f"Erreur de connexion à MySQL : {e}")
        raise


def create_table_if_not_exists(connection):
    """
    Crée la table `texts` si elle n'existe pas.
    """
    create_table_query = """
    CREATE TABLE IF NOT EXISTS texts (
        id INT AUTO_INCREMENT PRIMARY KEY,
        content TEXT NOT NULL
    );
    """
    cursor = connection.cursor()
    cursor.execute(create_table_query)
    connection.commit()
    print("Table 'texts' vérifiée/créée avec succès.")


def insert_data_into_mysql(connection, data):
    """
    Insère les données nettoyées dans la table MySQL.
    """
    cursor = connection.cursor()
    insert_query = "INSERT INTO texts (content) VALUES (%s)"
    for _, row in data.iterrows():
        cursor.execute(insert_query, (row['text'],))  # Utilise 'text' au lieu de 'content'
    connection.commit()
    print(f"{len(data)} lignes insérées dans la table 'texts'.")


def verify_insertion(connection):
    """
    Vérifie que les données ont bien été insérées.
    """
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM texts;")
    count = cursor.fetchone()[0]
    print(f"Nombre total de lignes dans la table 'texts' : {count}")

def validate_data(connection):
    """
    Valide les données en exécutant une requête SQL.
    """
    query = "SELECT COUNT(*) FROM texts WHERE content IS NOT NULL;"
    cursor = connection.cursor()
    cursor.execute(query)
    count = cursor.fetchone()[0]
    print(f"Nombre de lignes où 'content' n'est pas NULL : {count}")
    return count

def fetch_data_from_mysql(connection):
    """
    Récupère les données de la table MySQL 'texts'.
    """
    query = "SELECT * FROM texts;"
    cursor = connection.cursor(dictionary=True)  # Retourne les résultats sous forme de dictionnaires
    cursor.execute(query)
    results = cursor.fetchall()
    print(f"Nombre de lignes récupérées : {len(results)}")
    return results

def main():
    parser = argparse.ArgumentParser(description="Préparer les données pour le staging.")
    parser.add_argument('--bucket', type=str, required=True, help="Nom du bucket S3 contenant les données brutes.")
    parser.add_argument('--file-key', type=str, required=True, help="Clé du fichier dans le bucket S3.")
    parser.add_argument('--download-path', type=str, required=True, help="Chemin local pour le fichier téléchargé.")
    parser.add_argument('--endpoint-url', type=str, default="http://localhost:4566", help="URL de l'endpoint S3.")
    parser.add_argument('--mysql-host', type=str, default="127.0.0.1", help="Adresse de l'hôte MySQL.")
    parser.add_argument('--mysql-port', type=int, default=3306, help="Port MySQL.")
    parser.add_argument('--mysql-user', type=str, default="root", help="Utilisateur MySQL.")
    parser.add_argument('--mysql-password', type=str, default="root", help="Mot de passe MySQL.")
    parser.add_argument('--mysql-database', type=str, required=True, help="Base de données MySQL.")
    args = parser.parse_args()

    # Téléchargement des données depuis S3
    download_from_s3(args.bucket, args.file_key, args.download_path, args.endpoint_url)

    # Nettoyage des données
    cleaned_data = clean_data(args.download_path)

    # Connexion à MySQL
    connection = connect_to_mysql(args.mysql_host, args.mysql_port, args.mysql_user, args.mysql_password, args.mysql_database)

    try:
        # Création de la table si nécessaire
        create_table_if_not_exists(connection)

        # Insertion des données nettoyées
        insert_data_into_mysql(connection, cleaned_data)

        # Vérification de l'insertion
        verify_insertion(connection)

        # Validation des données
        validate_data(connection)

        # Récupération des données pour l'étape 'Curated'
        curated_data = fetch_data_from_mysql(connection)
        print("Exemple de données récupérées :", curated_data[:5])  # Affiche un échantillon
    finally:
        if connection.is_connected():
            connection.close()
            print("Connexion MySQL terminée.")


if __name__ == "__main__":
    main()
