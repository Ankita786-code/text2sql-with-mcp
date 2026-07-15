import duckdb

DB_PATH = "data/company.duckdb"


def validate_sql(sql):

    conn = duckdb.connect(DB_PATH)

    try:

        conn.execute("EXPLAIN " + sql)

        conn.close()

        return True

    except Exception as e:

        conn.close()

        print("\nValidation Error:")
        print(e)

        return False