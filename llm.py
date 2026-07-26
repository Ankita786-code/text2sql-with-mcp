import ollama

def generate_sql(question, table_name, schema):

    prompt = f"""
You are an expert Text-to-SQL assistant.

Your task is to generate a valid DuckDB SQL query that answers the user's natural language question.

Database Information

Table Name:
{table_name}

Schema:
{schema}

Instructions:
1. Generate exactly one DuckDB SQL query.
2. Use ONLY the table "{table_name}".
3. Use ONLY the columns listed in the schema.
4. Never invent table names.
5. Never invent column names.
6. Never invent values.
7. Preserve values exactly as they appear in the question whenever possible.
8. Use single quotes (' ') for all string literals.
9. Return ONLY the SQL query.
10. End the SQL query with a semicolon.

Question:
{question}

SQL:
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

    sql = response["message"]["content"].strip()

    # Remove markdown if present
    sql = sql.replace("```sql", "").replace("```", "").strip()

    return sql