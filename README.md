# TP4 - Data Processing Pipeline with Airflow
This project implements a three-step data processing pipeline using Airflow for orchestration.

You can also run the pipeline locally with DVC if desired.

## Architecture
The pipeline consists of three main steps:

* **Raw**: Extract source data to a raw zone
* **Staging**: Transform and load data into MySQL
* **Curated**: Final processing and storage in MongoDB

## Prerequisites
* Python 3.8+
* DVC
* MySQL
* MongoDB
* LocalStack (to simulate S3)

## How to Run
1. Run the command `docker-compose build`.
2. Start the services with `docker-compose up -d`.
3. Access the Airflow interface on `localhost:8081`. Replace `localhost` with the local IP of the VM or WSL 2 if necessary.
4. Log in to Airflow using the username and password **airflow** (pre-configured in the `docker-compose` file).
5. From your terminal, run the `pipeline.py` script in the `dags` folder. This will make the DAG appear in the Airflow web interface.
6. Trigger the DAG from the graphical interface. It will automatically rerun at the interval defined in `pipeline.py`.

This pipeline will continuously populate a database from an API, as will be further explored in TP5.
