import duckdb

conn = duckdb.connect("data/company.duckdb")

# Drop old tables
conn.execute("DROP TABLE IF EXISTS employee")
conn.execute("DROP TABLE IF EXISTS department")
conn.execute("DROP TABLE IF EXISTS project")

# Employee table
conn.execute("""
CREATE TABLE employee (
    id INTEGER PRIMARY KEY,
    name VARCHAR,
    age INTEGER,
    gender VARCHAR,
    department VARCHAR,
    salary INTEGER,
    hire_date DATE
)
""")

# Department table
conn.execute("""
CREATE TABLE department (
    dept_id INTEGER PRIMARY KEY,
    department_name VARCHAR,
    manager VARCHAR
)
""")

# Project table
conn.execute("""
CREATE TABLE project (
    project_id INTEGER PRIMARY KEY,
    project_name VARCHAR,
    department VARCHAR,
    budget INTEGER
)
""")

# Departments
conn.execute("""
INSERT INTO department VALUES
(1,'IT','Amit Roy'),
(2,'HR','Sneha Patel'),
(3,'Finance','Raj Mehta'),
(4,'Marketing','Pooja Sen'),
(5,'Sales','Arjun Kumar');
""")

# Employees
conn.execute("""
INSERT INTO employee VALUES
(1,'Alice',24,'Female','HR',50000,'2022-01-10'),
(2,'Bob',28,'Male','IT',70000,'2021-05-20'),
(3,'Charlie',31,'Male','Finance',65000,'2020-08-15'),
(4,'David',29,'Male','IT',80000,'2019-07-18'),
(5,'Eva',26,'Female','HR',55000,'2023-02-01'),
(6,'Frank',35,'Male','Sales',62000,'2020-11-12'),
(7,'Grace',27,'Female','Marketing',58000,'2022-06-14'),
(8,'Henry',30,'Male','IT',90000,'2018-09-25'),
(9,'Isabella',25,'Female','Finance',67000,'2023-03-18'),
(10,'Jack',32,'Male','Sales',72000,'2021-10-08'),
(11,'Kevin',29,'Male','IT',76000,'2022-04-12'),
(12,'Lily',24,'Female','Marketing',54000,'2024-01-20'),
(13,'Mia',28,'Female','Finance',69000,'2021-12-03'),
(14,'Noah',31,'Male','HR',61000,'2020-07-09'),
(15,'Olivia',27,'Female','IT',85000,'2023-05-17'),
(16,'Peter',33,'Male','Sales',64000,'2019-06-11'),
(17,'Queen',26,'Female','Marketing',57000,'2022-08-22'),
(18,'Ryan',34,'Male','Finance',78000,'2018-12-15'),
(19,'Sophia',29,'Female','HR',60000,'2021-09-05'),
(20,'Thomas',30,'Male','IT',82000,'2020-03-27');
""")

# Projects
conn.execute("""
INSERT INTO project VALUES
(101,'AI Chatbot','IT',500000),
(102,'Payroll System','HR',250000),
(103,'ERP Upgrade','Finance',800000),
(104,'Digital Marketing','Marketing',350000),
(105,'CRM Platform','Sales',450000);
""")

conn.commit()
conn.close()

print("Company database created successfully!")
