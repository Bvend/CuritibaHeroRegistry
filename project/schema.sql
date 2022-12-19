DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS person;
DROP TABLE IF EXISTS villain;

CREATE TABLE person (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nickname TEXT NOT NULL,
  bio TEXT,
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
  is_adm INTEGER NOT NULL,

  tier CHAR,
  
  id_person_id INTEGER,
  FOREIGN KEY (id_person_id) REFERENCES person(id)
);

CREATE TABLE villain (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  _status TEXT,
  
  id_person_id INTEGER,
  FOREIGN KEY (id_person_id) REFERENCES person(id)
);
