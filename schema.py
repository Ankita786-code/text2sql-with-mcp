import duckdb


DB_PATH = "data/company.duckdb"


def get_schema():
    conn = duckdb.connect(DB_PATH)

    schema = ""

    tables = conn.execute("SHOW TABLES").fetchall()

    for table in tables:

        table_name = table[0]

        schema += f"\nTable: {table_name}\n"

        columns = conn.execute(f"DESCRIBE {table_name}").fetchall()

        for col in columns:

            schema += f"{col[0]} ({col[1]})\n"

    conn.close()

    return schema