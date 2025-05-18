#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Run SQL Queries Script
This script runs all the SQL queries from the solutions.sql file and displays the results.
"""

import os
import sys
import pandas as pd
import psycopg2
from sqlalchemy import create_engine, text
from pathlib import Path
import re
from tabulate import tabulate
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database connection parameters
DB_PARAMS = {
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'database': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD')
}

def create_db_engine():
    """Create SQLAlchemy engine for database operations"""
    try:
        connection_string = f"postgresql://{DB_PARAMS['user']}:{DB_PARAMS['password']}@{DB_PARAMS['host']}:{DB_PARAMS['port']}/{DB_PARAMS['database']}"
        engine = create_engine(connection_string)
        print("Database engine created successfully")
        return engine
    except Exception as e:
        print(f"Error creating database engine: {e}")
        sys.exit(1)

def read_sql_file(file_path):
    """Read SQL queries from a file and split them into individual queries"""
    try:
        with open(file_path, 'r') as f:
            sql_content = f.read()
        
        # Split the SQL content into individual queries
        # This regex pattern looks for SQL statements ending with a semicolon
        # and ignores semicolons within comments
        queries = []
        current_query = ""
        lines = sql_content.split('\n')
        
        for line in lines:
            stripped_line = line.strip()
            
            # Skip empty lines
            if not stripped_line:
                current_query += line + "\n"
                continue
            
            # Handle comments
            if stripped_line.startswith('--'):
                current_query += line + "\n"
                continue
            
            # Add line to current query
            current_query += line + "\n"
            
            # Check if the line ends with a semicolon (end of query)
            if stripped_line.endswith(';'):
                queries.append(current_query.strip())
                current_query = ""
        
        return queries
    except Exception as e:
        print(f"Error reading SQL file: {e}")
        return []

def run_queries(engine, queries):
    """Run each SQL query and display the results"""
    for i, query in enumerate(queries, 1):
        # Skip empty queries
        if not query.strip():
            continue
        
        # Skip comments-only queries
        if all(line.strip().startswith('--') for line in query.split('\n') if line.strip()):
            continue
        
        # Extract query description from comments
        description = ""
        for line in query.split('\n'):
            if line.strip().startswith('--'):
                description += line.strip()[2:].strip() + " "
            else:
                break
        
        print(f"\n{'='*80}")
        print(f"Query {i}: {description.strip()}")
        print(f"{'='*80}")
        print(f"SQL: {query}")
        
        try:
            # Check if the query is a CREATE VIEW statement
            if "CREATE OR REPLACE VIEW" in query.upper():
                with engine.connect() as conn:
                    conn.execute(text(query))
                    conn.commit()
                print("View created successfully")
            else:
                # Execute the query and fetch results
                df = pd.read_sql_query(query, engine)
                
                # Display the results
                if not df.empty:
                    print(f"\nResults ({len(df)} rows):")
                    print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))
                else:
                    print("\nNo results returned")
        except Exception as e:
            print(f"Error executing query: {e}")

def main():
    """Main function to run SQL queries"""
    # Create database engine
    engine = create_db_engine()
    
    # Get the project root directory
    project_root = Path(__file__).parent.parent.parent
    sql_file = project_root / "src" / "sql" / "solutions.sql"
    
    # Read SQL queries from file
    queries = read_sql_file(sql_file)
    
    if not queries:
        print("No SQL queries found in the file")
        return
    
    # Run the queries
    run_queries(engine, queries)

if __name__ == "__main__":
    main() 