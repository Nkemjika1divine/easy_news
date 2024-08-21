CREATE DATABASE easy_news;
CREATE USER IF NOT EXISTS 'admin_en'@'localhost' IDENTIFIED BY 'en_admin';
GRANT ALL PRIVILEGES ON `easy_news`.* TO 'admin_en'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'admin_en'@'localhost';
FLUSH PRIVILEGES;