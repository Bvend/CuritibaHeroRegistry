DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS person;

CREATE TABLE person (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nickname TEXT NOT NULL,
  _description TEXT,
  _role INTEGER NOT NULL,

  _power TEXT,
  _zone TEXT,

  birth_day INTEGER,
  birth_month INTEGER,
  birth_year INTEGER,
  
  picture_url TEXT,
  class CHAR 
);

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  
  id_person_id INTEGER,
  FOREIGN KEY (id_person_id) REFERENCES person
);
