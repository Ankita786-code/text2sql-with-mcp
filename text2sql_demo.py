import duckdb

con = duckdb.connect("test.db")

question = input("Ask a question: ")

if "above 80" in question.lower():
    sql = "SELECT * FROM students WHERE marks > 80"

elif "all students" in question.lower():
    sql = "SELECT * FROM students"

elif "count students" in question.lower():
    sql = "SELECT COUNT(*) FROM students"

else:
    print("Question not supported")
    exit()

print("\nGenerated SQL:")
print(sql)

result = con.execute(sql).fetchall()

print("\nResult:")
print(result)