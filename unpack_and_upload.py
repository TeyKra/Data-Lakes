import os
import pandas as pd
import argparse
import boto3

def combine_files(input_dir, output_file):
    """
    Combine les fichiers train, test et dev en un seul fichier.
    """
    combined_df = pd.DataFrame()
    for split in ['train', 'test', 'dev']:
        file_path = os.path.join(input_dir, split, f'wikitext-2-raw-{split}.csv')
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            df['split'] = split  # Ajouter une colonne pour identifier l'origine des données
            combined_df = pd.concat([combined_df, df], ignore_index=True)
        else:
            print(f"Fichier manquant : {file_path}")
    
    # Enregistrer le fichier combiné
    combined_df.to_csv(output_file, index=False)
    print(f"Fichier combiné enregistré : {output_file}")
    return output_file

def upload_to_s3(file_path, bucket_name, endpoint_url):
    """
    Téléverse un fichier dans un bucket S3 LocalStack.
    """
    s3 = boto3.client('s3', endpoint_url=endpoint_url)
    bucket_key = os.path.basename(file_path)
    s3.upload_file(file_path, bucket_name, bucket_key)
    print(f"Fichier téléversé dans {bucket_name} avec le nom {bucket_key}")

def main():
    parser = argparse.ArgumentParser(description="Script d'unpacking pour combiner et téléverser des données.")
    parser.add_argument('--input-dir', type=str, required=True, help="Répertoire contenant les fichiers raw (train, test, dev).")
    parser.add_argument('--output-file', type=str, required=True, help="Chemin du fichier combiné à générer.")
    parser.add_argument('--bucket-name', type=str, required=True, help="Nom du bucket S3 où téléverser le fichier.")
    parser.add_argument('--endpoint-url', type=str, default="http://localhost:4566", help="URL de l'endpoint S3 (par défaut : LocalStack).")
    
    args = parser.parse_args()
    
    # Combiner les fichiers
    combined_file = combine_files(args.input_dir, args.output_file)
    
    # Téléverser dans le bucket raw
    upload_to_s3(combined_file, args.bucket_name, args.endpoint_url)

if __name__ == "__main__":
    main()
