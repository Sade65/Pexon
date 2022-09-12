-- SQLite
CREATE TABLE certs (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    name TEXT NOT NULL, 
    cert BLOB NOT NULL, 
    filename TEXT NOT NULL, 
    certname TEXT NOT NULL);


