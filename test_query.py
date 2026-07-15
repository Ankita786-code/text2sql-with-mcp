import duckdb

con = duckdb.connect("test.db")

con.execute("""
CREATE TABLE IF NOT EXISTS students(
    id INTEGER,
    name VARCHAR,
    marks INTEGER
)
""")

con.execute("""
INSERT INTO students VALUES
(1,'Alice',88),
(2,'Bob',72),
(3,'Carol',95)
""")

result = con.execute(
    "SELECT * FROM students WHERE marks > 80"
).fetchall()

print(result)