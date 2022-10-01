
CREATE TABLE IF NOT EXISTS archivage_files(
   file_id serial PRIMARY KEY ,
   checksum VARCHAR (100) NOT NULL,
   expiration_date DATE NOT NULL,
   filename VARCHAR (30) NOT NULL,
   is_valid Boolean default TRUE
);

CREATE OR REPLACE VIEW v_archivage_files AS
  SELECT 
  file_id ,
  checksum ,
filename ,
is_valid,
expiration_date,
  expiration_date < CURRENT_DATE AS "is_expired" 

FROM archivage_files;