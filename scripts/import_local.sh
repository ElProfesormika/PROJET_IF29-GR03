#!/bin/bash

DB_NAME="database_local1"
COLLECTION_NAME="tweets"
DATA_DIR="/home/el-professor/Téléchargements/IF29/raw"
MONGO_URI="mongodb://localhost:27017"

# Vérifier mongoimport
if ! command -v mongoimport &> /dev/null; then
  echo "mongoimport introuvable"
  exit 1
fi

# Vérifier MongoDB local
if ! mongosh --quiet --eval "db.runCommand({ ping: 1 })" &> /dev/null; then
  echo "MongoDB local non démarré"
  exit 1
fi

shopt -s nullglob
files=("$DATA_DIR"/*.json)

if [ ${#files[@]} -eq 0 ]; then
  echo "Attention : Aucun fichier JSON trouvé"
  exit 0
fi

echo "${#files[@]} fichiers détectés"

for file in "${files[@]}"; do
  echo "Import de $(basename "$file")..."
  mongoimport \
    --uri="$MONGO_URI" \
    --db="$DB_NAME" \
    --collection="$COLLECTION_NAME" \
    --file="$file" \
    --mode=insert \
    --numInsertionWorkers=4
done

echo "Import local terminé avec succès"
