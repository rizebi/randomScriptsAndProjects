PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE user (
	id INTEGER NOT NULL, 
	username VARCHAR(100), 
	password VARCHAR(100), 
	PRIMARY KEY (id), 
	UNIQUE (username)
);
COMMIT;
