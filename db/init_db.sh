#!/bin/bash
set -e
echo "Creating database..."
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" --password "$POSTGRES_PASSWORD" <<-EOSQL
   CREATE TABLE IF NOT EXISTS archivage_files(
   file_id serial PRIMARY KEY,
   checksum VARCHAR (100) NOT NULL,
   expiration_date DATE NOT NULL,
   file_name VARCHAR (20) NOT NULL
);
GO
CREATE OR REPLACE VIEW v_archivage_files AS
  SELECT 
  file_id ,
  checksum ,
file_name ,
expiration_date,
  expiration_date < current_date AS "is_expired" 

FROM archivage_files;
EOSQL
