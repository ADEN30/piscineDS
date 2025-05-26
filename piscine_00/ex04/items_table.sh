#!/bin/bash

FOLDER="/item/*.csv"
TABLE_NAME="items"
DB="piscineds"
USER="postgres"

for CSV_FILE in $FOLDER; do

	FILE_NAME=$(basename "$CSV_FILE" .csv)
	TABLE_NAME="$FILE_NAME" + "s"

	echo "Importing $CSV_FILE into table $TABLE_NAME..."


	psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" <<EOF
DROP TABLE IF EXISTS "$TABLE_NAME";

CREATE TABLE "$TABLE_NAME" (
	product_id INT,
	category_id BIGINT, 
	category_code TEXT,
	brand TEXT
);

COPY "$TABLE_NAME" FROM '$CSV_FILE' DELIMITER ',' CSV HEADER;
EOF

done