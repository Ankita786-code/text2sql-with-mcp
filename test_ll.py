from llm import generate_sql

question = input("Question: ")

sql = generate_sql(question)

print(sql)