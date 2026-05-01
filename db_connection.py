import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def get_db_connection():
    """Create and return a MySQL database connection"""
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
            port=os.getenv('DB_PORT', 3306)
        )
        
        if connection.is_connected():
            print("Connected to MySQL database")
            return connection
            
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def execute_query(connection, query, values=None):
    """Execute a SELECT query and return results"""
    try:
        cursor = connection.cursor()
        if values:
            cursor.execute(query, values)
        else:
            cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        return results
    except Error as e:
        print(f"Error executing query: {e}")
        return None

def execute_update(connection, query, values=None, verbose=True):
    """Execute INSERT, UPDATE, or DELETE query"""
    try:
        cursor = connection.cursor()
        if values:
            cursor.execute(query, values)
        else:
            cursor.execute(query)
        connection.commit()
        if verbose:
            print(f"Query executed successfully. Rows affected: {cursor.rowcount}")
        cursor.close()
        return True
    except Error as e:
        connection.rollback()
        print(f"Error executing update: {e}")
        return False
