import requests
import time
import json
import argparse
import boto3
from datetime import datetime

class HackerNewsAPI:
    BASE_URL = "https://hacker-news.firebaseio.com/v0"

    @staticmethod
    def get_top_stories(limit=50):
        """Récupère et retourne une liste des meilleures histoires."""
        stories = []
        
        # Récupération des IDs
        url = f"{HackerNewsAPI.BASE_URL}/topstories.json" # A vous de trouver l'URL exacte à query
        response = requests.get(url)
        story_ids = response.json()[:limit]
        
        # Récupération des détails pour chaque histoire
        for story_id in story_ids:
            url = f"{HackerNewsAPI.BASE_URL}/item/{story_id}.json" # A vous de trouver l'URL à query encore une fois
            response = requests.get(url)
            story = response.json()
            
            if story and story.get('type') == 'story':
                # Transformation des données directement
                transformed_story = {
                    "id": story.get("id"),
                    "title": story.get("title"),
                    "url": story.get("url", ""),
                    "score": story.get("score", 0),
                    "timestamp": datetime.fromtimestamp(story.get("time", 0)).isoformat()
                }
                stories.append(transformed_story)
            
            time.sleep(0.1)  # Pour éviter de surcharger l'API
        
        return stories

def upload_to_s3(stories, endpoint_url, bucket_name="raw-data", file_name="hacker_news_stories.json"):
    try:
        s3_client = boto3.client('s3', endpoint_url=endpoint_url)
        
        # Convertir les histoires en JSON
        data = json.dumps(stories, indent=4)
        
        # Uploader vers S3
        s3_client.put_object(
            Bucket=bucket_name,
            Key=file_name,
            Body=data,
            ContentType='application/json'
        )
        print(f"Fichier {file_name} uploadé avec succès dans le bucket {bucket_name}.")
    except Exception as e:
        print(f"Erreur lors de l'upload vers S3 : {e}")

def main():
    parser = argparse.ArgumentParser(description='Fetch top stories from Hacker News API')
    parser.add_argument('--limit', type=int, default=50,
                      help='Number of stories to fetch')
    parser.add_argument('--endpoint-url', type=str, default='http://localhost:4566',
                      help='URL du endpoint S3 (LocalStack)')
    
    args = parser.parse_args()
    
    # Récupération des histoires
    stories = HackerNewsAPI.get_top_stories(args.limit)
    
    # Upload vers S3
    upload_to_s3(stories, args.endpoint_url)

if __name__ == "__main__":
    main()