# TP5 - Data Processing Pipeline with Airflow
This project implements a three-step data processing pipeline using Airflow for orchestration.

You can always run the pipeline locally with DVC if desired nonetheless.

## Architecture
The pipeline consists of three main steps:

* Raw: Extract source data to a raw zone
* Staging: Transform and load data into MySQL
* Curated: Final processing and storage in MongoDB

## Prerequisites
Python 3.8+  
DVC  
MySQL  
MongoDB  
LocalStack (to simulate S3)

## Trigger the Airflow DAG from TP4

* Run a **docker-compose build** to install the virtual environment that will be used by Airflow. Airflow uses its own execution environment, which is why we no longer simply use a conda venv or similar, but a Dockerfile.
* Run **docker-compose up -d** to start all services.
* Access the Airflow interface at localhost:8081. If needed, replace `localhost` with the local IP address of the VM or WSL 2 instance where your stack is running. 
* I have configured the `docker-compose` to use **airflow** as the username and password.
* From your terminal, run the `pipeline.py` script located in the `dags` folder. This will make the DAG appear in the Airflow web interface.
* You can now trigger the DAG from the graphical interface. It will automatically be re-triggered at the interval defined in `pipeline.py`...
* ... which we will use to continuously populate a database from an API in TP5.

## Your Objective

* Follow the TP5 instructions to retrieve data from the HackerNews API.
* To do this, you need to complete three scripts: `src/hn_api.py`, `src/es_handler.py`, and `dags/hackernews_dag.py`.
* You can refer to the example from TP4 to make your DAG work.
