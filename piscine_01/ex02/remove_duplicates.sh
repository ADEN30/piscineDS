#!/bin/bash

psql -U $POSTGRES_USER -d $POSTGRES_DB -t -c \
	"DELETE FROM customers a
	USING (
	SELECT ctid, 
			ROW_NUMBER() OVER (
			PARTITION BY event_time, event_type, product_id, price, user_id, user_session
			ORDER BY ctid
			) AS rn
	FROM customers
	) b
	WHERE a.ctid = b.ctid AND b.rn > 1;"

psql -U $POSTGRES_USER -d $POSTGRES_DB -t -c \
	"DELETE FROM customers a
	USING (
	SELECT t1.ctid AS ctid_to_delete
	FROM customers t1
	JOIN customers t2
		ON t1.event_type = t2.event_type
	AND t1.price = t2.price
	AND t1.user_id = t2.user_id
	AND t1.user_session = t2.user_session
	AND t1.product_id = t2.product_id
	AND t1.event_time < t2.event_time
	AND t2.event_time - t1.event_time < INTERVAL '2 second'
	) to_delete
	WHERE a.ctid = to_delete.ctid_to_delete;"
