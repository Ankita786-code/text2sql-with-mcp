import duckdb

conn = duckdb.connect("data/company.duckdb")

conn.execute("""
CREATE TABLE IF NOT EXISTS employee(
    id INTEGER,
    name VARCHAR,
    department VARCHAR,
    salary INTEGER
)
""")

# Clear old data so inserts don't duplicate rows
conn.execute("DELETE FROM employee")

conn.execute("""
INSERT INTO employee VALUES
(1,'Alice','HR',50000),
(2,'Bob','IT',70000),
(3,'Charlie','Finance',65000),
(4,'David','IT',80000),
(5,'Eva','HR',55000)
""")

print("Database initialized successfully!")