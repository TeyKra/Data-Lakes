from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
from elasticsearch import Elasticsearch
import json

# Configuration des arguments par défaut pour le DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),  # Date de début
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

# Initialisation du DAG
dag = DAG(
    'hackernews_pipeline',
    default_args=default_args,
    description='Pipeline pour récupérer et indexer des données Hacker News dans Elasticsearch',
    schedule_interval='*/5 * * * *',  # Planification toutes les 5 minutes
    catchup=False,  # Éviter d'exécuter des runs passés
)

# Fonction pour récupérer les données depuis l'API Hacker News
def fetch_hackernews_stories():
    url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    response = requests.get(url)
    story_ids = response.json()[:50]  # Limiter à 50 histoires
    stories = []

    for story_id in story_ids:
        story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
        story_response = requests.get(story_url)
        story_data = story_response.json()

        if story_data and story_data.get("type") == "story":
            stories.append({
                "id": story_data.get("id"),
                "title": story_data.get("title"),
                "url": story_data.get("url", ""),
                "score": story_data.get("score", 0),
                "timestamp": datetime.fromtimestamp(story_data.get("time", 0)).isoformat(),
            })

    # Sauvegarder les données dans un fichier temporaire pour la tâche suivante
    with open('/tmp/hackernews_stories.json', 'w') as f:
        f.write(json.dumps(stories, indent=4))
    print(f"{len(stories)} histoires récupérées et sauvegardées.")

# Fonction pour indexer les données dans Elasticsearch
def index_stories_to_elasticsearch():
    es = Elasticsearch(hosts=[{"host": "elasticsearch", "port": 9200}])
    index_name = "hackernews"

    # Charger les données depuis le fichier temporaire
    with open('/tmp/hackernews_stories.json', 'r') as f:
        stories = json.load(f)

    # Indexation des données
    for story in stories:
        es.index(index=index_name, id=story["id"], body=story)
    print(f"{len(stories)} histoires indexées dans Elasticsearch.")

# Définir les tâches
fetch_data = PythonOperator(
    task_id='fetch_hackernews_stories',
    python_callable=fetch_hackernews_stories,
    dag=dag,
)

index_data = PythonOperator(
    task_id='index_stories_to_elasticsearch',
    python_callable=index_stories_to_elasticsearch,
    dag=dag,
)

# Définir l'ordre d'exécution des tâches
fetch_data >> index_data
