

"""
Database configuration for JudgmentCalcNV
Simple database connection setup
"""
import mysql.connector

# Database configuration
DB_CONFIG = {
    'host': 'database-1.ctnfprzjtuyt.us-east-1.rds.amazonaws.com',
    'user': 'admin',
    'password': 'yourpassword',
    'database': 'yourdatabase',
    'port': 1
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

