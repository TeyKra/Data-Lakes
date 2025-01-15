from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional
import boto3
import json
import mysql.connector
from pymongo import MongoClient
from datetime import datetime

app = FastAPI(title="Data Lake API")

# Configuration des connexions avec les bons paramètres
class DatabaseConnections:
    def __init__(self):
        # S3 (LocalStack)
        self.s3_client = boto3.client(
            's3',
            endpoint_url='http://localstack:4566'
        )
            
        
        # MySQL
        self.mysql_config = {
            'host': 'mysql',
            'user': 'root',
            'password': 'root',
            'database': 'nom_de_votre_bdd'
        }
        
        # MongoDB
        self.mongo_uri = 'mongodb://mongodb:27017/'
        self.mongo_client = MongoClient(self.mongo_uri)
        self.mongo_db = self.mongo_client['nom_de_votre_db']

db = DatabaseConnections()

@app.get("/raw/", response_model=List[dict])
async def get_raw_stories(
    limit: Optional[int] = Query(10, description="Nombre maximum de stories à retourner"),
    min_score: Optional[int] = Query(None, description="Score minimum des stories")
):
    """
    Récupère les stories depuis le bucket S3 raw
    """
    try:
        response = db.s3_client.get_object(
            Bucket='raw',
            Key='nom_des_stories_hackernews_dans_raw.json'
        )
        stories = json.loads(response['Body'].read().decode('utf-8'))
        
        # Filtrage
        if min_score is not None:
            stories = [story for story in stories if story.get('score', 0) >= min_score]
        
        return stories[:limit]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la lecture depuis S3: {str(e)}")

@app.get("/staging/", response_model=List[dict])
async def get_warehouse_stories(
    start_date: Optional[str] = Query(None, description="Date de début (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="Date de fin (YYYY-MM-DD)"),
    min_score: Optional[int] = Query(None, description="Score minimum")
):
    """
    Récupère les stories depuis MySQL (warehouse)
    """
    try:
        conn = mysql.connector.connect(**db.mysql_config)
        cursor = conn.cursor(dictionary=True)
        
        query = "SELECT * FROM stories WHERE 1=1"
        params = []
        
        if start_date:
            query += " AND DATE(timestamp) >= %s"
            params.append(start_date)
        
        if end_date:
            query += " AND DATE(timestamp) <= %s"
            params.append(end_date)
            
        if min_score:
            query += " AND score >= %s"
            params.append(min_score)
            
        cursor.execute(query, params)
        stories = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        # Convertir les datetime en str pour la sérialisation JSON
        for story in stories:
            if 'timestamp' in story:
                story['timestamp'] = story['timestamp'].isoformat()
        
        return stories
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la lecture depuis MySQL: {str(e)}")

@app.get("/curated/", response_model=List[dict])
async def get_story_stats(
    time_window: Optional[str] = Query("daily", description="Fenêtre temporelle (daily, weekly, monthly)"),
    min_stories: Optional[int] = Query(None, description="Nombre minimum de stories")
):
    """
    Récupère les statistiques depuis MongoDB
    """
    try:
        collection = db.mongo_db.story_stats
        
        # Construction de la requête
        query = {}
        if min_stories:
            query["story_count"] = {"$gte": min_stories}
        
        if time_window:
            query["time_window"] = time_window
            
        # Exclure le champ _id de MongoDB
        stats = list(collection.find(query, {'_id': 0}))
        
        # Convertir les dates en format ISO pour la sérialisation JSON
        for stat in stats:
            if 'date' in stat:
                stat['date'] = stat['date'].isoformat()
        
        return stats
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la lecture depuis MongoDB: {str(e)}")

@app.get("/health")
async def health_check():
    """
    Vérifie la santé de l'API et des connexions aux bases de données
    """
    status = {
        "api_status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "connections": {}
    }
    
    try:
        # Test S3
        db.s3_client.list_buckets()
        status["connections"]["s3"] = True
    except:
        status["connections"]["s3"] = False
    
    try:
        # Test MySQL
        conn = mysql.connector.connect(**db.mysql_config)
        conn.close()
        status["connections"]["mysql"] = True
    except:
        status["connections"]["mysql"] = False
    
    try:
        # Test MongoDB
        db.mongo_client.server_info()
        status["connections"]["mongodb"] = True
    except:
        status["connections"]["mysql"] = False
    
    return status

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)