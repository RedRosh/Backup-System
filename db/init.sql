
CREATE TABLE IF NOT EXISTS archivage_files(
   file_id serial PRIMARY KEY AUTO,
   checksum VARCHAR (100) NOT NULL,
   expiration_date DATE NOT NULL,
   filename VARCHAR (20) NOT NULL
);

CREATE OR REPLACE VIEW v_archivage_files AS
  SELECT 
  file_id ,
  checksum ,
filename ,
expiration_date,
  expiration_date < current_date AS "is_expired" 

FROM archivage_files;