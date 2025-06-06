#!/bin/bash

# Connexion à PostgreSQL
psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" <<EOF

-- Étape 1 : Ajouter les colonnes manquantes à la table customers
DO \$\$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'customers' AND column_name = 'product_id'
    ) THEN
        ALTER TABLE customers ADD COLUMN product_id UUID;
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'customers' AND column_name = 'category_id'
    ) THEN
        ALTER TABLE customers ADD COLUMN category_id BIGINT;
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'customers' AND column_name = 'category_code'
    ) THEN
        ALTER TABLE customers ADD COLUMN category_code TEXT;
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'customers' AND column_name = 'brand'
    ) THEN
        ALTER TABLE customers ADD COLUMN brand TEXT;
    END IF;
END
\$\$;
EOF

echo "Creation des indexs..."
psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" <<EOF
-- Étape 2 : Création d'un index pour optimiser la jointure
CREATE INDEX IF NOT EXISTS idx_customers_product_id ON customers(product_id);
CREATE INDEX IF NOT EXISTS idx_items_product_id ON items(product_id);
EOF
echo "fin de la creation des indexs"

echo "MAJ des donnees"

psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" <<EOF
-- Étape 3 : Mettre à jour les données depuis la table items
UPDATE customers
SET
    category_id = items.category_id,
    category_code = items.category_code,
    brand = items.brand
FROM items
WHERE customers.product_id = items.product_id;
EOF


