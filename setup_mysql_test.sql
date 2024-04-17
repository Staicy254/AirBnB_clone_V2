-- Prepares the MySQL server for the AirBnB test environment and project

-- Create the project testing database named 'hbnb_test_db'
CREATE DATABASE IF NOT EXISTS hbnb_test_db;

-- Create a new user named 'hbnb_test' with all privileges on the database 'hbnb_test_db'
-- and set the password to 'hbnb_test_pwd' if it doesn't exist
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';

-- Grant the SELECT privilege for user 'hbnb_test' on the 'performance_schema' database
GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';

-- Flush privileges after granting SELECT privilege
FLUSH PRIVILEGES;

-- Grant all privileges to user 'hbnb_test' on the database 'hbnb_test_db'
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost';

-- Flush privileges after granting privileges
FLUSH PRIVILEGES;

