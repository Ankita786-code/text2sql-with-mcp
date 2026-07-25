# sql_converter.py

def clean_column(column_name):
    """
    Convert WikiSQL column names into SQL-safe column names.
    """
    return (
        column_name.replace(" ", "_")
        .replace("(", "")
        .replace(")", "")
        .replace("-", "_")
        .replace(".", "")
        .replace("/", "_")
    )


def logical_form_to_sql(logical_form, columns, table_name):
    """
    Convert WikiSQL logical form into executable SQL.
    """

    agg_map = {
        0: "",
        1: "MAX",
        2: "MIN",
        3: "COUNT",
        4: "SUM",
        5: "AVG"
    }

    op_map = {
        0: "=",
        1: ">",
        2: "<"
    }

    # SELECT column
    select_column = clean_column(columns[logical_form["sel"]])

    agg = agg_map.get(logical_form["agg"], "")

    if agg:
        select_clause = f"{agg}({select_column})"
    else:
        select_clause = select_column

    sql = f"SELECT {select_clause} FROM {table_name}"

    # WHERE conditions
    if logical_form["conds"]:

        conditions = []

        for condition in logical_form["conds"]:

            column_index, operator, value = condition

            column = clean_column(columns[column_index])

            operator_symbol = op_map.get(operator, "=")

            # Numeric values shouldn't be quoted
            try:
                float(value)
                value_string = str(value)
            except:
                value_string = f"'{value}'"

            conditions.append(
                f"{column} {operator_symbol} {value_string}"
            )

        sql += " WHERE " + " AND ".join(conditions)

    sql += ";"

    return sql