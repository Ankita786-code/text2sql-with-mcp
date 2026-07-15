import ollama
from schema import get_schema


def generate_sql(question):

    schema = get_schema()

    prompt = f"""
You are a DuckDB SQL expert.

Database Schema:

{schema}

Rules:
1. Return ONLY SQL.
2. No explanation.
3. No markdown.
4. End with ;

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