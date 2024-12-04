import os
import pandas as pd
import argparse
import boto3

def combine_files(input_dir, output_file):
    """
    Combine the train, test, and dev files into a single file.
    """
    combined_df = pd.DataFrame()
    for split in ['train', 'test', 'dev']:
        file_path = os.path.join(input_dir, split, f'wikitext-2-raw-{split}.csv')
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            df['split'] = split  # Add a column to identify the origin of the data
            combined_df = pd.concat([combined_df, df], ignore_index=True)
        else:
            print(f"Missing file: {file_path}")
    
    # Save the combined file
    combined_df.to_csv(output_file, index=False)
    print(f"Combined file saved: {output_file}")
    return output_file

def upload_to_s3(file_path, bucket_name, endpoint_url):
    """
    Uploads a file to an S3 bucket in LocalStack.
    """
    s3 = boto3.client('s3', endpoint_url=endpoint_url)
    bucket_key = os.path.basename(file_path)
    s3.upload_file(file_path, bucket_name, bucket_key)
    print(f"File uploaded to {bucket_name} with the name {bucket_key}")

def main():
    parser = argparse.ArgumentParser(description="Unpacking script to combine and upload data.")
    parser.add_argument('--input-dir', type=str, required=True, help="Directory containing the raw files (train, test, dev).")
    parser.add_argument('--output-file', type=str, required=True, help="Path to the combined file to be generated.")
    parser.add_argument('--bucket-name', type=str, required=True, help="Name of the S3 bucket to upload the file.")
    parser.add_argument('--endpoint-url', type=str, default="http://localhost:4566", help="S3 endpoint URL (default: LocalStack).")
    
    args = parser.parse_args()
    
    # Combine the files
    combined_file = combine_files(args.input_dir, args.output_file)
    
    # Upload to the raw bucket
    upload_to_s3(combined_file, args.bucket_name, args.endpoint_url)

if __name__ == "__main__":
    main()
