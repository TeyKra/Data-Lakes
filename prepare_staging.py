import os
import pandas as pd
import mysql.connector
from mysql.connector import Error
import boto3
import argparse


def download_from_s3(bucket_name, file_key, download_path, endpoint_url):
    """
    Downloads a file from an S3 bucket.
    """
    s3 = boto3.client('s3', endpoint_url=endpoint_url)
    s3.download_file(bucket_name, file_key, download_path)
    print(f"File downloaded from S3: {file_key} -> {download_path}")


def clean_data(file_path):
    """
    Cleans the data: removes duplicates and empty rows.
    """
    df = pd.read_csv(file_path)
    print("Available columns in the file:", df.columns)  # Debug
    original_count = len(df)
    df.drop_duplicates(inplace=True)
    df.dropna(inplace=True)
    cleaned_count = len(df)
    print(f"Data cleaned: {original_count - cleaned_count} rows removed.")
    return df


def connect_to_mysql(host, port, user, password, database):
    """
    Establishes a connection to the MySQL database.
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
            print(f"Connected to MySQL database: {database}")
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        raise


def create_table_if_not_exists(connection):
    """
    Creates the `texts` table if it does not already exist.
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
    print("Table 'texts' successfully verified/created.")


def insert_data_into_mysql(connection, data):
    """
    Inserts cleaned data into the MySQL table.
    """
    cursor = connection.cursor()
    insert_query = "INSERT INTO texts (content) VALUES (%s)"
    for _, row in data.iterrows():
        cursor.execute(insert_query, (row['text'],))  # Uses 'text' instead of 'content'
    connection.commit()
    print(f"{len(data)} rows inserted into the 'texts' table.")


def verify_insertion(connection):
    """
    Verifies that data has been successfully inserted.
    """
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM texts;")
    count = cursor.fetchone()[0]
    print(f"Total rows in the 'texts' table: {count}")


def validate_data(connection):
    """
    Validates the data by executing an SQL query.
    """
    query = "SELECT COUNT(*) FROM texts WHERE content IS NOT NULL;"
    cursor = connection.cursor()
    cursor.execute(query)
    count = cursor.fetchone()[0]
    print(f"Number of rows where 'content' is not NULL: {count}")
    return count


def fetch_data_from_mysql(connection):
    """
    Fetches data from the MySQL 'texts' table.
    """
    query = "SELECT * FROM texts;"
    cursor = connection.cursor(dictionary=True)  # Returns results as dictionaries
    cursor.execute(query)
    results = cursor.fetchall()
    print(f"Number of rows retrieved: {len(results)}")
    return results


def main():
    parser = argparse.ArgumentParser(description="Prepare data for staging.")
    parser.add_argument('--bucket', type=str, required=True, help="Name of the S3 bucket containing raw data.")
    parser.add_argument('--file-key', type=str, required=True, help="Key of the file in the S3 bucket.")
    parser.add_argument('--download-path', type=str, required=True, help="Local path for the downloaded file.")
    parser.add_argument('--endpoint-url', type=str, default="http://localhost:4566", help="S3 endpoint URL.")
    parser.add_argument('--mysql-host', type=str, default="127.0.0.1", help="MySQL host address.")
    parser.add_argument('--mysql-port', type=int, default=3306, help="MySQL port.")
    parser.add_argument('--mysql-user', type=str, default="root", help="MySQL user.")
    parser.add_argument('--mysql-password', type=str, default="root", help="MySQL password.")
    parser.add_argument('--mysql-database', type=str, required=True, help="MySQL database name.")
    args = parser.parse_args()

    # Download data from S3
    download_from_s3(args.bucket, args.file_key, args.download_path, args.endpoint_url)

    # Clean the data
    cleaned_data = clean_data(args.download_path)

    # Connect to MySQL
    connection = connect_to_mysql(args.mysql_host, args.mysql_port, args.mysql_user, args.mysql_password, args.mysql_database)

    try:
        # Create table if necessary
        create_table_if_not_exists(connection)

        # Insert cleaned data
        insert_data_into_mysql(connection, cleaned_data)

        # Verify the insertion
        verify_insertion(connection)

        # Validate the data
        validate_data(connection)

        # Fetch data for the 'Curated' step
        curated_data = fetch_data_from_mysql(connection)
        print("Sample retrieved data:", curated_data[:5])  # Display a sample
    finally:
        if connection.is_connected():
            connection.close()
            print("MySQL connection closed.")


if __name__ == "__main__":
    main()
