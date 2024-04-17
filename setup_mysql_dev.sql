-- Prepares the MySQL server for the AirBnB clone project

-- Create the project development database named 'hbnb_dev_db'
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;

-- Create a new user named 'hbnb_dev' with all privileges on the database 'hbnb_dev_db'
-- and set the password to 'hbnb_dev_pwd' if it doesn't exist
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';

-- Grant all privileges to user 'hbnb_dev' on the database 'hbnb_dev_db'
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';

-- Flush privileges after granting privileges
FLUSH PRIVILEGES;

-- Grant SELECT privilege for user 'hbnb_dev' on the 'performance_schema' database
GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';

-- Flush privileges after granting SELECT privilege
FLUSH PRIVILEGES;

