"""
File: schema.py

Purpose:
This module extracts the schema of the DuckDB database.
The extracted schema is provided to the Large Language Model (LLM)
to help generate valid SQL queries using only the available
tables and columns.
"""

import duckdb

# Path to the DuckDB database
DB_PATH = "data/company.duckdb"


def get_schema():
    """
    Retrieves the schema of all tables in the DuckDB database.

    Returns:
        str: A formatted string containing the names of all tables
             and their corresponding columns with data types.
    """

    # Connect to the DuckDB database
    conn = duckdb.connect(DB_PATH)

    # Stores the complete database schema as a string
    schema = ""

    # Get all table names from the database
    tables = conn.execute("SHOW TABLES").fetchall()

    # Loop through each table
    for table in tables:

        table_name = table[0]

        # Add the table name to the schema string
        schema += f"\nTable: {table_name}\n"

        # Retrieve all columns of the current table
        columns = conn.execute(f"DESCRIBE {table_name}").fetchall()

        # Add each column name and data type
        for col in columns:
            schema += f"{col[0]} ({col[1]})\n"

    # Close the database connection
    conn.close()

    # Return the complete schema
    return schema