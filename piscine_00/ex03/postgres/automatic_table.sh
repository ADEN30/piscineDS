#!/bin/bash

FOLDER="/customer/*.csv"
TABLE_NAME="data_2022_oct"
DB="piscineds"
USER="postgres"

for CSV_FILE in $FOLDER; do

	FILE_NAME=$(basename "$CSV_FILE" .csv)
	TABLE_NAME="$FILE_NAME"

	echo "Importing $CSV_FILE into table $TABLE_NAME..."


	psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" <<EOF
DROP TABLE IF EXISTS "$TABLE_NAME";

CREATE TABLE "$TABLE_NAME" (
	event_time TIMESTAMP,
	event_type TEXT,
	product_id BIGINT,
	price REAL,
	user_id BIGINT,
	user_session UUID
);

COPY "$TABLE_NAME" FROM '$CSV_FILE' DELIMITER ',' CSV HEADER;
EOF

done

