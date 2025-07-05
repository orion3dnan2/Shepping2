#!/usr/bin/env python3
"""
MySQL Database Setup Script for Shipping Management System
This script creates a MySQL database connection for testing purposes.
"""

import os
import subprocess
import time
from sqlalchemy import create_engine, text

def setup_mysql_database():
    """Set up a MySQL database for the shipping management system."""
    
    # Database configuration
    db_name = "shipping_db"
    db_user = "root"
    db_password = "password123"
    db_host = "localhost"
    db_port = "3306"
    
    # Create DATABASE_URL environment variable
    database_url = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    
    print(f"Setting DATABASE_URL to: mysql+pymysql://{db_user}:***@{db_host}:{db_port}/{db_name}")
    
    # Set environment variable
    os.environ["DATABASE_URL"] = database_url
    
    # Create .env file for persistent storage
    with open('.env', 'w') as f:
        f.write(f"DATABASE_URL={database_url}\n")
        f.write(f"SESSION_SECRET=your-secret-key-here\n")
    
    print("MySQL configuration completed!")
    print("DATABASE_URL has been set in environment and .env file")
    
    return database_url

if __name__ == "__main__":
    setup_mysql_database()