import duckdb

conn = duckdb.connect("data/company.duckdb")

result = conn.execute("SELECT * FROM employee").fetchall()

for row in result:
    print(row)