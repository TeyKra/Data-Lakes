from elasticsearch import Elasticsearch
import json
import argparse
import boto3
from io import BytesIO

class ElasticsearchHandler:
    def __init__(self, host="localhost", port=9200):
        # Activez le mode de compatibilité pour Elasticsearch 7.x
        self.es = Elasticsearch(
            hosts=[{'host': host, 'port': port, 'scheme': 'http'}],
            compatibility_mode=True
        )

    def create_index(self, index_name="hackernews"):
        mappings = {
            "mappings": {
                "properties": {
                    "id": {"type": "integer"},
                    "title": {"type": "text"},
                    "url": {"type": "keyword"},
                    "score": {"type": "integer"},
                    "timestamp": {"type": "date"}
                }
            }
        }
        self.es.indices.create(index=index_name, body=mappings, ignore=400)
        print(f"Index '{index_name}' créé avec succès.")

    def index_stories(self, stories, index_name="hackernews"):
        for story in stories:
            self.es.index(index=index_name, id=story["id"], body=story)
        print(f"{len(stories)} stories indexées dans l'index '{index_name}'.")

def get_stories_from_s3(endpoint_url, bucket_name="raw-data", file_name="hacker_news_stories.json"):
    try:
        s3_client = boto3.client('s3', endpoint_url=endpoint_url)
        response = s3_client.get_object(Bucket=bucket_name, Key=file_name)
        content = response['Body'].read().decode('utf-8')
        return json.loads(content)
    except Exception as e:
        print(f"Erreur lors de la récupération des stories depuis S3 : {e}")
        return []

def main():
    parser = argparse.ArgumentParser(description='Index stories to Elasticsearch')
    parser.add_argument('--host', type=str, default='elasticsearch',
                      help='Elasticsearch host')
    parser.add_argument('--port', type=int, default=9200,
                      help='Elasticsearch port')
    parser.add_argument('--index', type=str, default='hackernews',
                      help='Elasticsearch index name')
    parser.add_argument('--endpoint-url', type=str, default='http://localhost:4566',
                      help='URL du endpoint S3 (LocalStack)')
    
    args = parser.parse_args()
    
    # Récupération des stories depuis S3
    stories = get_stories_from_s3(args.endpoint_url)
    
    # Indexation dans Elasticsearch
    es_handler = ElasticsearchHandler(host=args.host, port=args.port)
    es_handler.index_stories(stories, args.index)

if __name__ == "__main__":
    main()