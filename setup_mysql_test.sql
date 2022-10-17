-- prepares a MySQL server for the project
-- create project developement database with the name : hbnb_test_db
CREATE DATABASE IF NOT EXISTS hbnb_test_db;
-- creating new user named : hbnb_test
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';
-- granting all privileges to the new user
GRANT ALL PRIVILEGES ON `hbnb_test_db`.* TO 'hbnb_test'@'localhost';
-- granting the SELECT privilege for the user hbnb_test in the db performance_schema
GRANT SELECT ON `performance_schema`.* TO 'hbnb_test'@'localhost';
FLUSH PRIVILEGES;
