SET search_path TO ate;

CREATE TABLE badcolumncount AS
  SELECT table1.text
  FROM table1 JOIN table2 ON table1.id = table2.foreign_id;
