import os
from datasets import load_dataset

# Définir les chemins des répertoires
base_dir = 'data/raw'
subdirs = ['train', 'test', 'dev']

# Créer les répertoires s'ils n'existent pas
for subdir in subdirs:
    path = os.path.join(base_dir, subdir)
    os.makedirs(path, exist_ok=True)

# Télécharger le jeu de données wikitext-2-raw-v1
dataset = load_dataset("wikitext", "wikitext-2-raw-v1")

# Enregistrer les fichiers dans les répertoires correspondants
dataset["train"].to_csv(os.path.join(base_dir, 'train', 'wikitext-2-raw-train.csv'), index=False)
dataset["test"].to_csv(os.path.join(base_dir, 'test', 'wikitext-2-raw-test.csv'), index=False)
dataset["validation"].to_csv(os.path.join(base_dir, 'dev', 'wikitext-2-raw-dev.csv'), index=False)
