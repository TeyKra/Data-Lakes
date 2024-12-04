import os
from datasets import load_dataset

# Define directory paths
base_dir = 'data/raw'
subdirs = ['train', 'test', 'dev']

# Create directories if they don't already exist
for subdir in subdirs:
    path = os.path.join(base_dir, subdir)
    os.makedirs(path, exist_ok=True)

# Download the wikitext-2-raw-v1 dataset
dataset = load_dataset("wikitext", "wikitext-2-raw-v1")

# Save the files into their corresponding directories
dataset["train"].to_csv(os.path.join(base_dir, 'train', 'wikitext-2-raw-train.csv'), index=False)
dataset["test"].to_csv(os.path.join(base_dir, 'test', 'wikitext-2-raw-test.csv'), index=False)
dataset["validation"].to_csv(os.path.join(base_dir, 'dev', 'wikitext-2-raw-dev.csv'), index=False)
