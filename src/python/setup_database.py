import psycopg2
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def connect_to_database():
    """Connect to PostgreSQL database"""
    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )
        print("Database connection established successfully")
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        sys.exit(1)

def execute_sql_file(conn, file_path):
    """Execute SQL commands from a file"""
    try:
        with open(file_path, 'r') as f:
            sql_content = f.read()
        
        cursor = conn.cursor()
        cursor.execute(sql_content)
        conn.commit()
        cursor.close()
        print(f"Successfully executed SQL file: {file_path}")
    except Exception as e:
        print(f"Error executing SQL file {file_path}: {e}")
        conn.rollback()

def setup_database():
    """Set up the database with schema and initial data"""
    conn = connect_to_database()
    
    # Get the project root directory
    project_root = Path(__file__).parent.parent.parent
    sql_dir = project_root / "sql"
    
    # Execute schema.sql first to create tables
    schema_file = sql_dir / "schema.sql"
    execute_sql_file(conn, schema_file)
    
    # Execute data files in order
    data_files = [
        "products.sql",
        "users.sql",
        "orders.sql",
        "reviews.sql"
    ]
    
    for file_name in data_files:
        file_path = sql_dir / file_name
        print(f"Loading data from {file_path}...")
        execute_sql_file(conn, file_path)
    
    conn.close()
    print("Database setup completed successfully")

if __name__ == "__main__":
    setup_database() 