SET search_path TO ate;

CREATE TABLE badrowcontentsnoorder AS
  SELECT CAST(CONCAT(table1.text, 'X') AS varchar(50)) AS text, table2.number
  FROM table1 JOIN table2 ON table1.id = table2.foreign_id;
