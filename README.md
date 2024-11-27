# Data Lakes & Data Integration 

This repository is designed to help students learn about data lakes and data integration pipelines using Python, Docker, LocalStack, and DVC. Follow the steps below to set up and run the pipeline.

---

## 1. Prerequisites

### Install Docker
Docker is required to run LocalStack, a tool simulating AWS services locally.

1. Install Docker:
```bash
sudo apt update
sudo apt install docker.io
```

2. Verify Docker installation:
```bash
docker --version
```

3. Install AWS CLI
AWS CLI is used to interact with LocalStack S3 buckets.
```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

4. Verify that the installation worked
```bash
aws --version
```

5. Configure AWS CLI for LocalStack
```bash
aws configure
```

Enter the following values:
* AWS Access Key ID: root
* AWS Secret Access Key: root
* Default region name: us-east-1
* Default output format: json

6. Create LocalStack S3 buckets:

Install localstack :
```bash
pip install localstack
```

Start localstack :
```bash
localstack start
```
```bash
    __                     _______ __             __
    / /   ____  _________ _/ / ___// /_____ ______/ /__
   / /   / __ \/ ___/ __ `/ /\__ \/ __/ __ `/ ___/ //_/
  / /___/ /_/ / /__/ /_/ / /___/ / /_/ /_/ / /__/ ,<
 /_____/\____/\___/\__,_/_//____/\__/\__,_/\___/_/|_|

 💻 LocalStack CLI 4.0.2
 👤 Profile: default

[13:52:07] starting LocalStack in Docker mode 🐳                                  localstack.py:510
           container image not found on host                                      bootstrap.py:1297
[13:55:42] download complete                                                      bootstrap.py:1301
────────────────────────── LocalStack Runtime Log (press CTRL-C to quit) ──────────────────────────

LocalStack version: 4.0.3.dev7
LocalStack build date: 2024-11-26
LocalStack build git hash: 5f19fbc6b

Ready.
```

Copy the code:
```bash
aws --endpoint-url=http://localhost:4566 s3 mb s3://raw
aws --endpoint-url=http://localhost:4566 s3 mb s3://staging
aws --endpoint-url=http://localhost:4566 s3 mb s3://curated
```

Localstack output:
```bash
2024-11-26T15:38:51.684  INFO --- [et.reactor-0] localstack.request.aws     : AWS s3.CreateBucket => 200
2024-11-26T15:38:57.947  INFO --- [et.reactor-0] localstack.request.aws     : AWS s3.CreateBucket => 200
2024-11-26T15:39:03.247  INFO --- [et.reactor-0] localstack.request.aws     : AWS s3.CreateBucket => 200

check if your endpoint are created:  
```bash
aws --endpoint-url=http://localhost:4566 s3 ls                      

2024-11-26 14:03:05 raw
2024-11-26 14:03:31 staging
2024-11-26 14:03:37 curated
```

7. Install DVC
   
DVC is used for data version control and pipeline orchestration.
```bash
pip install dvc
```

```bash
dvc remote add -d localstack-s3 s3://
dvc remote modify localstack-s3 endpointurl http://localhost:4566
```

## 2. Repository Setup

Install Python Dependencies
```bash
pip install -r build/requirements.txt
```

Download the Dataset
```bash
pip install kaggle 
kaggle datasets download googleai/pfam-seed-random-split
```

Move the dataset into a data/raw folder.

## 3. Running the Pipeline

Unpack the dataset into a single CSV file in the raw bucket:
```bash
python build/unpack_to_raw.py --input_dir data/raw --bucket_name raw --output_file_name combined_raw.csv

Processing file: data/raw/train/data-00005-of-00080
Processing file: data/raw/train/data-00004-of-00080
Processing file: data/raw/train/data-00072-of-00080
Processing file: data/raw/train/data-00073-of-00080
Processing file: data/raw/train/data-00046-of-00080
Processing file: data/raw/train/data-00047-of-00080
Processing file: data/raw/train/data-00078-of-00080
Processing file: data/raw/train/data-00079-of-00080
Processing file: data/raw/train/data-00031-of-00080
Processing file: data/raw/train/data-00030-of-00080
Processing file: data/raw/train/data-00012-of-00080
Processing file: data/raw/train/data-00013-of-00080
Processing file: data/raw/train/data-00065-of-00080
Processing file: data/raw/train/data-00064-of-00080
Processing file: data/raw/train/data-00018-of-00080
Processing file: data/raw/train/data-00019-of-00080
Processing file: data/raw/train/data-00051-of-00080
Processing file: data/raw/train/data-00050-of-00080
Processing file: data/raw/train/data-00026-of-00080
Processing file: data/raw/train/data-00027-of-00080
Processing file: data/raw/train/data-00015-of-00080
Processing file: data/raw/train/data-00014-of-00080
Processing file: data/raw/train/data-00062-of-00080
Processing file: data/raw/train/data-00063-of-00080
Processing file: data/raw/train/data-00056-of-00080
Processing file: data/raw/train/data-00057-of-00080
Processing file: data/raw/train/data-00021-of-00080
Processing file: data/raw/train/data-00020-of-00080
Processing file: data/raw/train/data-00068-of-00080
Processing file: data/raw/train/data-00069-of-00080
Processing file: data/raw/train/data-00002-of-00080
Processing file: data/raw/train/data-00003-of-00080
Processing file: data/raw/train/data-00075-of-00080
Processing file: data/raw/train/data-00074-of-00080
Processing file: data/raw/train/data-00041-of-00080
Processing file: data/raw/train/data-00040-of-00080
Processing file: data/raw/train/data-00008-of-00080
Processing file: data/raw/train/data-00009-of-00080
Processing file: data/raw/train/data-00036-of-00080
Processing file: data/raw/train/data-00037-of-00080
Processing file: data/raw/train/data-00052-of-00080
Processing file: data/raw/train/data-00053-of-00080
Processing file: data/raw/train/data-00025-of-00080
Processing file: data/raw/train/data-00024-of-00080
Processing file: data/raw/train/data-00058-of-00080
Processing file: data/raw/train/data-00059-of-00080
Processing file: data/raw/train/data-00011-of-00080
Processing file: data/raw/train/data-00010-of-00080
Processing file: data/raw/train/data-00066-of-00080
Processing file: data/raw/train/data-00067-of-00080
Processing file: data/raw/train/data-00045-of-00080
Processing file: data/raw/train/data-00044-of-00080
Processing file: data/raw/train/data-00032-of-00080
Processing file: data/raw/train/data-00033-of-00080
Processing file: data/raw/train/data-00006-of-00080
Processing file: data/raw/train/data-00007-of-00080
Processing file: data/raw/train/data-00038-of-00080
Processing file: data/raw/train/data-00039-of-00080
Processing file: data/raw/train/data-00071-of-00080
Processing file: data/raw/train/data-00070-of-00080
Processing file: data/raw/train/data-00042-of-00080
Processing file: data/raw/train/data-00043-of-00080
Processing file: data/raw/train/data-00035-of-00080
Processing file: data/raw/train/data-00034-of-00080
Processing file: data/raw/train/data-00001-of-00080
Processing file: data/raw/train/data-00000-of-00080
Processing file: data/raw/train/data-00048-of-00080
Processing file: data/raw/train/data-00049-of-00080
Processing file: data/raw/train/data-00076-of-00080
Processing file: data/raw/train/data-00077-of-00080
Processing file: data/raw/train/data-00055-of-00080
Processing file: data/raw/train/data-00054-of-00080
Processing file: data/raw/train/data-00022-of-00080
Processing file: data/raw/train/data-00023-of-00080
Processing file: data/raw/train/data-00016-of-00080
Processing file: data/raw/train/data-00017-of-00080
Processing file: data/raw/train/data-00061-of-00080
Processing file: data/raw/train/data-00060-of-00080
Processing file: data/raw/train/data-00028-of-00080
Processing file: data/raw/train/data-00029-of-00080
Processing file: data/raw/test/data-00004-of-00010
Processing file: data/raw/test/data-00005-of-00010
Processing file: data/raw/test/data-00009-of-00010
Processing file: data/raw/test/data-00008-of-00010
Processing file: data/raw/test/data-00003-of-00010
Processing file: data/raw/test/data-00002-of-00010
Processing file: data/raw/test/data-00007-of-00010
Processing file: data/raw/test/data-00006-of-00010
Processing file: data/raw/test/data-00000-of-00010
Processing file: data/raw/test/data-00001-of-00010
Processing file: data/raw/dev/data-00004-of-00010
Processing file: data/raw/dev/data-00005-of-00010
Processing file: data/raw/dev/data-00009-of-00010
Processing file: data/raw/dev/data-00008-of-00010
Processing file: data/raw/dev/data-00003-of-00010
Processing file: data/raw/dev/data-00002-of-00010
Processing file: data/raw/dev/data-00007-of-00010
Processing file: data/raw/dev/data-00006-of-00010
Processing file: data/raw/dev/data-00000-of-00010
Processing file: data/raw/dev/data-00001-of-00010
Combined CSV saved to /tmp/combined_raw.csv
File uploaded to S3 bucket 'raw' with key 'combined_raw.csv'
Temporary file /tmp/combined_raw.csv removed.
```

Check if the combined_raw.csv is into the raw bucket: 
```bash 
% aws --endpoint-url=http://localhost:4566 s3 ls s3://raw/ --recursive

2024-11-26 14:38:33  651149365 combined_raw.csv
```

Localstack output:
```bash
2024-11-26T13:38:33.628  INFO --- [et.reactor-0] localstack.request.aws     : AWS s3.CreateMultipartUpload => 200
2024-11-26T13:38:34.421  INFO --- [et.reactor-7] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:34.424  INFO --- [et.reactor-6] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:34.429  INFO --- [et.reactor-3] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:34.430  INFO --- [et.reactor-8] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:34.433  INFO --- [et.reactor-2] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:34.434  INFO --- [et.reactor-1] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:34.435  INFO --- [et.reactor-0] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:34.435  INFO --- [et.reactor-4] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:34.436  INFO --- [et.reactor-5] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:34.439  INFO --- [et.reactor-9] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:35.035  INFO --- [et.reactor-9] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:35.060  INFO --- [et.reactor-7] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:35.061  INFO --- [et.reactor-8] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:35.066  INFO --- [et.reactor-1] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:35.068  INFO --- [et.reactor-4] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:35.071  INFO --- [et.reactor-2] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:35.074  INFO --- [et.reactor-0] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:35.075  INFO --- [et.reactor-6] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:35.077  INFO --- [et.reactor-3] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:35.078  INFO --- [et.reactor-5] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:35.557  INFO --- [et.reactor-9] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:35.615  INFO --- [et.reactor-8] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:35.675  INFO --- [et.reactor-7] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:35.683  INFO --- [et.reactor-5] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:35.696  INFO --- [et.reactor-2] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:35.697  INFO --- [et.reactor-6] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:35.708  INFO --- [et.reactor-1] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:35.743  INFO --- [et.reactor-3] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:35.747  INFO --- [et.reactor-0] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:35.760  INFO --- [et.reactor-4] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:36.144  INFO --- [et.reactor-9] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:36.229  INFO --- [et.reactor-7] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:36.299  INFO --- [et.reactor-8] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:36.320  INFO --- [et.reactor-2] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:36.371  INFO --- [et.reactor-4] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:36.372  INFO --- [et.reactor-3] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:36.374  INFO --- [et.reactor-5] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:36.376  INFO --- [et.reactor-6] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:36.380  INFO --- [et.reactor-0] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:36.381  INFO --- [et.reactor-1] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:36.592  INFO --- [et.reactor-9] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:36.948  INFO --- [et.reactor-7] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:37.094  INFO --- [et.reactor-8] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:37.113  INFO --- [et.reactor-5] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:37.204  INFO --- [et.reactor-1] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:37.220  INFO --- [et.reactor-2] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:37.222  INFO --- [et.reactor-6] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:37.229  INFO --- [et.reactor-4] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:37.239  INFO --- [et.reactor-3] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:37.246  INFO --- [et.reactor-0] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:37.309  INFO --- [et.reactor-9] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:37.542  INFO --- [et.reactor-7] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:37.703  INFO --- [et.reactor-8] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:37.829  INFO --- [et.reactor-2] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:37.956  INFO --- [et.reactor-5] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:37.965  INFO --- [et.reactor-4] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:37.981  INFO --- [et.reactor-6] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:37.999  INFO --- [et.reactor-0] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:38.001  INFO --- [et.reactor-1] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:38.002  INFO --- [et.reactor-3] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:38.010  INFO --- [et.reactor-9] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:38.199  INFO --- [et.reactor-9] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:38.346  INFO --- [et.reactor-7] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:38.352  INFO --- [et.reactor-8] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:38.462  INFO --- [et.reactor-2] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:38.494  INFO --- [et.reactor-5] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:38.510  INFO --- [et.reactor-1] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:38.515  INFO --- [et.reactor-6] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:38.535  INFO --- [et.reactor-3] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:38.536  INFO --- [et.reactor-4] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:38.540  INFO --- [et.reactor-0] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:38.743  INFO --- [et.reactor-9] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:38.802  INFO --- [et.reactor-8] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:38.819  INFO --- [et.reactor-7] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:38.829  INFO --- [et.reactor-5] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:38.856  INFO --- [et.reactor-2] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:38.875  INFO --- [et.reactor-4] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:38.879  INFO --- [et.reactor-6] localstack.request.aws     : AWS s3.UploadPart => 200
2024-11-26T13:38:41.423  INFO --- [et.reactor-1] localstack.request.aws     : AWS s3.CompleteMultipartUpload => 200
```

Preprocess the data to clean, encode, split into train/dev/test, and compute class weights:
```bash
python src/preprocess_to_staging.py --bucket_raw raw --bucket_staging staging --input_file combined_raw.csv --output_prefix preprocessed

Downloading raw data from S3...
Splitting data into train, dev, and test sets...
Train data uploaded to S3 at preprocessed/train.csv
Dev data uploaded to S3 at preprocessed/dev.csv
Test data uploaded to S3 at preprocessed/test.csv
Class weights uploaded to S3.
```

Check if the files are into the staging bucket:
```bash
morgan@macbook-air-de-senechal Data-Lakes % aws --endpoint-url=http://localhost:4566 s3 ls s3://staging/ --recursive

2024-11-26 15:13:09   16296981 preprocessed/class_weights.txt
2024-11-26 15:12:45       2556 preprocessed/dev.csv
2024-11-26 14:51:47   38945379 preprocessed/label_encoder.joblib
2024-11-26 14:51:50   37831776 preprocessed/label_mapping.txt
2024-11-26 15:13:02  660746783 preprocessed/test.csv
2024-11-26 15:12:45       2556 preprocessed/train.csv
```

Localstack output:
```bash
2024-11-26T15:54:02.730  INFO --- [et.reactor-1] localstack.request.aws     : AWS s3.GetObject => 200
2024-11-26T16:12:11.335  INFO --- [et.reactor-2] localstack.request.aws     : AWS s3.PutObject => 200
2024-11-26T16:12:11.344  INFO --- [et.reactor-6] localstack.request.aws     : AWS s3.PutObject => 200
2024-11-26T16:12:33.714  INFO --- [et.reactor-8] localstack.request.aws     : AWS s3.PutObject => 200
2024-11-26T16:12:36.815  INFO --- [et.reactor-0] localstack.request.aws     : AWS s3.PutObject => 200
```

Prepare the data for model training by tokenizing sequences:
```bash
python src/process_to_curated.py \
    --bucket_staging staging \
    --bucket_curated curated \
    --input_file preprocessed/train.csv \
    --output_file tokenized_train.csv

Downloading preprocessed/train.csv from bucket staging...
Loading tokenizer for model facebook/esm2_t6_8M_UR50D...
Tokenizing sequences...
Creating tokenized DataFrame...
Merging tokenized sequences with metadata...
Saving processed data locally...
Uploading tokenized_train.csv to bucket curated...
Processed file successfully uploaded to curated/tokenized_train.csv.
```

Check if the files are into the curated bucket:
```bash
morgan@macbook-air-de-senechal Data-Lakes % aws --endpoint-url=http://localhost:4566 s3 ls s3://curated/ --recursive

2024-11-26 15:33:09      79955 tokenized_train.csv
```

Localstack output:
```bash
2024-11-26T14:37:17.393  INFO --- [et.reactor-3] localstack.request.aws     : AWS s3.GetObject => 200
2024-11-26T14:37:17.655  INFO --- [et.reactor-9] localstack.request.aws     : AWS s3.PutObject => 200
```

## 4. Running the Entire Pipeline with DVC
The pipeline stages are defined in dvc.yaml. Run the pipeline using:
```bash
dvc repro
```

## 5. Notes
Ensure LocalStack is running before executing any pipeline stage.
This pipeline illustrates a basic ETL flow for a data lake, preparing data from raw to curated for AI model training.
If you encounter any issues, ensure Docker, AWS CLI, and DVC are correctly configured.

