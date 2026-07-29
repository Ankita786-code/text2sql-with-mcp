"""
File: app_vanilla.py

Purpose:
This file implements the Vanilla Text-to-SQL pipeline.

Workflow:
1. Accepts a natural language question from the user.
2. Retrieves the database schema.
3. Sends the question and schema to the LLM.
4. Generates a DuckDB SQL query.
5. Validates the generated SQL query.
6. Executes the SQL query directly using DuckDB.
7. Displays the query result.

Unlike the MCP pipeline, this implementation executes SQL
directly using DuckDB without the MCP server.
"""

import duckdb

from schema import get_schema
from llm import generate_sql
from validator import validate_sql

# Path to the DuckDB database
DB_PATH = "data/company.duckdb"

# Create a connection to the database
conn = duckdb.connect(DB_PATH)

# Read the user's natural language question
question = input("Ask your question: ")

# Retrieve the database schema
schema = get_schema()

# Generate SQL using the LLM
sql = generate_sql(question, schema)

# Display the generated SQL query
print("\nGenerated SQL:\n")
print(sql)

# Validate the generated SQL before execution
if validate_sql(sql):

    # Execute the SQL query directly using DuckDB
    result = conn.execute(sql).fetchall()

    print("\nResult:\n")

    # Display each row of the query result
    for row in result:
        print(row)

else:
    print("\nSQL Validation Failed")