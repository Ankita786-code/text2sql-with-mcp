import ollama

def generate_sql(question, table_name, schema):

    prompt = f"""
You are an expert in DuckDB SQL.

Table Name:
{table_name}

Schema:
{schema}

Rules:
1. Use ONLY the table name "{table_name}".
2. Use ONLY the columns listed in the schema.
3. Do NOT invent tables or columns.
4. Do NOT invent values.
5. Use single quotes (' ') for string values.
6. Return ONLY the SQL query.
7. End the query with a semicolon.

Question:
{question}
"""

    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"].strip()