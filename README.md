# Text2SQL with MCP

## Overview

This project implements a Text-to-SQL application using DuckDB and Ollama. It converts natural language queries into SQL queries and executes them on a DuckDB database. The project also explores the integration of the Model Context Protocol (MCP).

## Tech Stack

- Python 3.14
- DuckDB
- Ollama (Llama 3.2)
- DuckDB Python API
- SQL
- Git & GitHub
- Visual Studio Code
- MCP SDK (currently being explored)

## Project Structure

```
text2sql-with-mcp/
│
├── app.py
├── create_database.py
├── llm.py
├── schema.py
├── server.py
├── validator.py
├── text2sql_demo.py
├── test_db.py
├── test_ll.py
├── test_query.py
├── data/
├── duckdb_mcp/
├── ai_usage/
├── README.md
├── requirements.txt
└── .gitignore
```

## Features

- Natural Language to SQL conversion
- SQL execution using DuckDB
- LLM-based SQL generation using Ollama
- MCP integration (experimental)
- Query validation
