import ollama
import re

# Choose the model
MODEL_NAME = "deepseek-coder:6.7b"
# MODEL_NAME = "llama3.2"


def generate_sql(question, table_name, schema):

    prompt = f"""
You are an expert Text-to-SQL assistant specialized in DuckDB.

Your task is to generate exactly ONE valid DuckDB SQL query that answers the user's natural language question.

Table Name:
{table_name}

Schema:
{schema}

Instructions:
1. Generate the SQL query that answers the given question.
2. Use ONLY the table "{table_name}".
3. Use ONLY the columns listed in the schema.
4. Never invent table names.
5. Never invent column names.
6. Never invent values.
7. Preserve values exactly as they appear in the question whenever possible.
8. Use single quotes (' ') for all string literals.
9. Return ONLY the SQL query.
10. Do NOT explain anything.
11. Do NOT use Markdown.
12. End the SQL query with a semicolon.

Question:
{question}

SQL:
"""

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    sql = response["message"]["content"].strip()

    # Remove markdown if present
    sql = sql.replace("```sql", "")
    sql = sql.replace("```", "")
    sql = sql.strip()

    # Extract only the SQL query
    match = re.search(
        r"(SELECT|WITH).*?;",
        sql,
        flags=re.IGNORECASE | re.DOTALL
    )

    if match:
        return match.group(0).strip()

    return sql