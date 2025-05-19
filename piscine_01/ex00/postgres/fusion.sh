#!/bin/bash

psql -U $POSTGRES_USER -d $POSTGRES_DB <<EOF

-- Création de la table fusionnée avec toutes les colonnes
DROP TABLE IF EXISTS merged_all;

SELECT
    event_time::TIMESTAMP,
    event_type::TEXT,
    product_id::INT,
    price::REAL,
    user_id::BIGINT,
    user_session::UUID
FROM customers

UNION

SELECT
    NULL::TIMESTAMP,
    NULL::TEXT,
    product_id,
    NULL::REAL,
    NULL::BIGINT,
    NULL::UUID
FROM item;



EOF

