import duckdb

from llm import generate_sql

from validator import validate_sql


DB_PATH = "data/company.duckdb"

conn = duckdb.connect(DB_PATH)

question = input("Ask your question: ")

sql = generate_sql(question)

print("\nGenerated SQL:\n")

print(sql)

if validate_sql(sql):

    result = conn.execute(sql).fetchall()

    print("\nResult:\n")

    for row in result:

        print(row)

else:

    print("\nSQL Validation Failed")