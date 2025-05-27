#!/bin/bash

MERGED_TABLE="customers"

# Motif pour filtrer les tables à fusionner (par exemple toutes les tables commençant par "table_")
TABLE_PREFIX="data_20"

# # Exporter le mot de passe pour éviter le prompt
# export PGPASSWORD="$POSTGRES_PASSWORD"

# Récupération des noms de table à fusionner
tables=$(psql -U "$POSTGRES_USER" -h "$DB_HOST" -d "$POSTGRES_DB" -t -c \
    "SELECT tablename FROM pg_tables WHERE schemaname = 'public' AND tablename LIKE '${TABLE_PREFIX}%';")

# Nettoyage de la liste (trim)
tables=$(echo "$tables" | xargs)

# Vérification
if [[ -z "$tables" ]]; then
  echo "Aucune table trouvée avec le préfixe '$TABLE_PREFIX'"
  exit 1
fi

# Supprimer l'ancienne table de fusion si elle existe
psql -U "$POSTGRES_USER" -h "$POSTGRES_HOST" -d "$POSTGRES_DB" -c "DROP TABLE IF EXISTS $MERGED_TABLE;"

# Créer la table fusionnée à partir de la structure de la première table
first_table=$(echo "$tables" | awk '{print $1}')
psql -U "$POSTGRES_USER" -h "$POSTGRES_HOST" -d "$POSTGRES_DB" -c \
    "CREATE TABLE $MERGED_TABLE (LIKE $first_table INCLUDING ALL);"

# Insérer les données de toutes les tables
for table in $tables; do
  echo "Fusion de la table $table..."
  psql -U "$POSTGRES_USER" -h "$POSTGRES_HOST" -d "$POSTGRES_DB" -c \
      "INSERT INTO $MERGED_TABLE SELECT * FROM $table;"
done
