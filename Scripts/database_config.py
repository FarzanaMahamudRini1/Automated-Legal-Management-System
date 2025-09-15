#!/usr/bin/env python
# coding: utf-8

# In[ ]:


"""
Database configuration for JudgmentCalcNV
Simple database connection setup
"""
import mysql.connector

# Database configuration
DB_CONFIG = {
    'host': 'database-1.ctnfprzjtuyt.us-east-1.rds.amazonaws.com',
    'user': 'admin',
    'password': 'Dnnbmstn1jrg',
    'database': 'DataWarehouse',
    'port': 3306
}

def get_database_connection():
    """Create and return database connection"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return None

def get_database_cursor():
    """Get database cursor"""
    connection = get_database_connection()
    if connection:
        return connection.cursor(), connection
    return None, None

