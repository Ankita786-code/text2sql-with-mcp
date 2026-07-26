from llm import generate_sql
from sql_converter import logical_form_to_sql

import json
import pandas as pd
import duckdb
import jsonlines
import random
import re


def create_duckdb_eval_suite(sample_size=50):

    print("🔄 Loading WikiSQL from local files...")

    # Load questions
    questions = []
    with jsonlines.open("test.jsonl") as reader:
        for row in reader:
            questions.append(row)

    random.seed(42)
    random.shuffle(questions)

    sampled_data = questions[:sample_size]

    # Load tables
    tables = {}
    with jsonlines.open("test.tables.jsonl") as reader:
        for table in reader:
            tables[table["id"]] = table

    eval_records = []

    print(f"📦 Creating {sample_size} DuckDB tables...")

    con = duckdb.connect(database=":memory:")

    for idx, item in enumerate(sampled_data):

        table_name = f"table_{idx}"

        table = tables[item["table_id"]]

        header = table["header"]
        rows = table["rows"]

        df = pd.DataFrame(rows, columns=header)

        # Clean column names
        cleaned_columns = []

        for c in df.columns:
            cleaned_columns.append(
                re.sub(r'[^a-zA-Z0-9_]', '_', c)
            )

        df.columns = cleaned_columns

        # Register table
        con.register(table_name, df)

        # Schema text for LLM
        schema_text = ""

        for col, dtype in zip(df.columns, df.dtypes):
            schema_text += f"{col} ({dtype})\n"

        # Schema dictionary (for printing)
        schema_dict = dict(zip(df.columns, [str(x) for x in df.dtypes]))

        # Ground Truth SQL
        ground_truth_sql = logical_form_to_sql(
            item["sql"],
            header,
            table_name
        )

        eval_records.append({

            "question": item["question"],

            "table_name": table_name,

            "schema_text": schema_text,

            "schema_dict": schema_dict,

            "ground_truth_sql": ground_truth_sql

        })

    print("✅ Evaluation suite ready!")

    return con, eval_records


# ---------------- MAIN ----------------

db, tests = create_duckdb_eval_suite(sample_size=50)

print("\n========== Text2SQL Evaluation ==========\n")

correct = 0
total = len(tests)

for i, test in enumerate(tests, start=1):

    print("=" * 70)

    print(f"Test Case {i}")

    print("\nQuestion:")
    print(test["question"])

    print("\nTable:")
    print(test["table_name"])

    print("\nSchema:")
    print(json.dumps(test["schema_dict"], indent=2))

    # LLM SQL
    generated_sql = generate_sql(
        test["question"],
        test["table_name"],
        test["schema_text"]
    )
    print("\nGenerated SQL:")
    print(generated_sql)

    print("\nGenerated SQL:")
    print(generated_sql)

    print("\nGround Truth SQL:")
    print(test["ground_truth_sql"])

    # Execute LLM SQL
    try:
        llm_result = db.execute(generated_sql).fetchall()
    except Exception as e:
        llm_result = f"Execution Error: {e}"

    # Execute Ground Truth SQL
    try:
        gt_result = db.execute(test["ground_truth_sql"]).fetchall()
    except Exception as e:
        gt_result = f"Execution Error: {e}"

    print("\nLLM Result:")
    print(llm_result)

    print("\nGround Truth Result:")
    print(gt_result)

    if llm_result == gt_result:
        print("\n✅ MATCH")
        correct += 1
    else:
        print("\n❌ NOT MATCH")

print("\n" + "=" * 70)
print("Evaluation Summary")
print("=" * 70)

print(f"Total Test Cases : {total}")
print(f"Matched          : {correct}")
print(f"Not Matched      : {total - correct}")
print(f"Accuracy         : {(correct / total) * 100:.2f}%")

print("\n✅ Evaluation Completed.")