
# TP5 - Data Processing Pipeline with Airflow

This project implements a three-stage data processing pipeline orchestrated using Airflow.  
Alternatively, you can run the pipeline locally using DVC if desired.

## Architecture

The pipeline consists of three main stages:

1. **Raw:** Extracting source data into a raw zone.  
2. **Staging:** Transforming and loading data into MySQL.  
3. **Curated:** Final processing and storage in MongoDB.  

## Prerequisites

To run this project, ensure the following are installed:

- Python 3.8+  
- DVC  
- MySQL  
- MongoDB  
- LocalStack (to simulate S3)  

## Triggering the Airflow DAG from TP4

1. Run `docker-compose build` to set up the virtual environment used by Airflow.  
   Airflow uses its own execution environment; therefore, we use a Dockerfile instead of a standard virtual environment like Conda.  

2. Run `docker-compose up -d` to launch all services.  

3. Access the Airflow interface at `http://localhost:8081`.  
   If necessary, replace `localhost` with the local IP address of your VM or WSL 2 instance running the stack.  
   The default credentials are:  
   - **Username:** `airflow`  
   - **Password:** `airflow`  

4. From your terminal, execute the `pipeline.py` script located in the `dags` folder.  
   This will make the DAG appear in the Airflow web interface.  

5. Trigger the DAG from the graphical interface.  
   It will automatically rerun at the interval defined in `pipeline.py`...  

6. ...which will be used to continuously populate a database from an API in TP5.  

## Your Objective

Follow the TP5 instructions to fetch data from the HackerNews API.  

### Required Scripts to Complete

- `src/hn_api.py`  
- `src/es_handler.py`  
- `dags/hackernews_dag.py`  

You can refer to the TP4 example to help you set up and run your DAG.  

### Sample Commands

#### Fetching Data
```bash
python hn_api.py --limit 50 --endpoint-url http://localhost:4566
```

**Output:**
`File hacker_news_stories.json successfully uploaded to the raw-data bucket.`  

#### Indexing Data
```bash
python es_handler.py --host localhost --port 9200 --endpoint-url http://localhost:4566
```

**Output:**
`49 stories indexed in the 'hackernews' index.`  

#### Querying Data
```bash
curl -X GET "http://localhost:9200/hackernews/_search?q=*&pretty"
```

**Output:**
```json
{
  "took" : 502,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 49,
      "relation" : "eq"
    },
    "max_score" : 1.0,
    "hits" : [
      {
        "_index" : "hackernews",
        "_type" : "_doc",
        "_id" : "42633501",
        "_score" : 1.0,
        "_source" : {
          "id" : 42633501,
          "title" : "We Cracked a 512-Bit DKIM Key for Less Than $8 in the Cloud",
          "url" : "https://dmarcchecker.app/articles/crack-512-bit-dkim-rsa-key",
          "score" : 209,
          "timestamp" : "2025-01-08T13:32:34"
        }
      }
      // ...additional results...
    ]
  }
}
```

## Airflow pipeline 

```bash
flowchart LR
    subgraph DAG: hackernews_pipeline
    A[fetch_hackernews_stories] --> B[index_stories_to_elasticsearch]
    end
```

