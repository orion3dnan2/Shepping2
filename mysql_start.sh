#!/bin/bash
# Start MySQL server script
echo "Starting MySQL server..."
mysqld --datadir=./mysql_data_local --port=3306 --socket=/tmp/mysql.sock --user=root --skip-networking &
MYSQL_PID=$!

# Wait for MySQL to start
sleep 5

# Create shipping database
echo "Creating shipping database..."
mysql -u root -p'dyYOY6-#_&pz' -e "CREATE DATABASE IF NOT EXISTS shipping_db;"
mysql -u root -p'dyYOY6-#_&pz' -e "ALTER USER 'root'@'localhost' IDENTIFIED BY 'password123';"
mysql -u root -p'dyYOY6-#_&pz' -e "FLUSH PRIVILEGES;"

echo "MySQL setup completed!"
echo "MySQL PID: $MYSQL_PID"