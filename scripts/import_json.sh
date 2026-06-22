#!/bin/bash

DB_NAME="database01"
COLLECTION_NAME="collection01"
DATA_DIR="/home/el-professor/Téléchargements/IF29/raw"
MONGO_URI="mongodb+srv://housseni0:h2lLb9Er6ouOAyUq@cluster1if29.je0onrx.mongodb.net/database01"

if ! command -v mongoimport &> /dev/null; then
  echo "mongoimport introuvable"
  exit 1
fi

shopt -s nullglob
files=("$DATA_DIR"/*.json)

if [ ${#files[@]} -eq 0 ]; then
  echo "Attention : Aucun fichier JSON trouvé"
  exit 0
fi

for file in "${files[@]}"; do
  echo "Import de $(basename "$file")..."
  mongoimport \
    --uri="$MONGO_URI" \
    --collection="$COLLECTION_NAME" \
    --file="$file" \
    --verbose
done

echo "Import terminé avec succès"
