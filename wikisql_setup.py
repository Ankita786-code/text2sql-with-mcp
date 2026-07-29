"""
File: wikisql_setup.py

Purpose:
This module evaluates the Text-to-SQL system using the WikiSQL
benchmark dataset.

Workflow:
1. Load WikiSQL questions and tables.
2. Create temporary DuckDB tables for evaluation.
3. Generate SQL queries using the LLM.
4. Execute both generated and ground-truth SQL queries.
5. Compare their execution results.
6. Calculate the overall accuracy.
7. Save all failed test cases for further analysis.
"""

from llm_wikisql import generate_sql
from sql_converter import logical_form_to_sql

import json
import pandas as pd
import duckdb
import jsonlines
import random
import re


def create_duckdb_eval_suite(sample_size=50):
    """
    Creates an evaluation environment using randomly selected
    WikiSQL test cases.

    Parameters:
        sample_size (int):
            Number of WikiSQL test cases to evaluate.

    Returns:
        tuple:
            DuckDB connection object and evaluation records.
    """

    print("🔄 Loading WikiSQL from local files...")

    # Load all WikiSQL questions
    questions = []

    with jsonlines.open("test.jsonl") as reader:
        for row in reader:
            questions.append(row)

    # Shuffle questions for random evaluation
    random.seed(42)
    random.shuffle(questions)

    # Select the required number of test cases
    sampled_data = questions[:sample_size]

    # Load all WikiSQL tables
    tables = {}

    with jsonlines.open("test.tables.jsonl") as reader:
        for table in reader:
            tables[table["id"]] = table

    eval_records = []

    print(f"📦 Creating {sample_size} DuckDB tables...")

    # Create an in-memory DuckDB database
    con = duckdb.connect(database=":memory:")

    # Process every selected WikiSQL sample
    for idx, item in enumerate(sampled_data):

        table_name = f"table_{idx}"

        table = tables[item["table_id"]]

        header = table["header"]
        rows = table["rows"]

        # Convert table rows into a DataFrame
        df = pd.DataFrame(rows, columns=header)

        # Clean column names to make them SQL compatible
        cleaned_columns = []

        for c in df.columns:
            cleaned_columns.append(
                re.sub(r'[^a-zA-Z0-9_]', '_', c)
            )

        df.columns = cleaned_columns

        # Register the DataFrame as a DuckDB table
        con.register(table_name, df)

        # Build schema text for the LLM
        schema_text = ""

        for col, dtype in zip(df.columns, df.dtypes):
            schema_text += f"{col} ({dtype})\n"

        # Dictionary used for displaying the schema
        schema_dict = dict(
            zip(
                df.columns,
                [str(x) for x in df.dtypes]
            )
        )

        # Convert WikiSQL logical form into SQL
        ground_truth_sql = logical_form_to_sql(
            item["sql"],
            header,
            table_name
        )

        # Store all information required for evaluation
        eval_records.append({

            "question": item["question"],

            "table_name": table_name,

            "schema_text": schema_text,

            "schema_dict": schema_dict,

            "ground_truth_sql": ground_truth_sql

        })

    print("✅ Evaluation suite ready!")

    return con, eval_records


# ============================================================
# Main Evaluation
# ============================================================

# Create a fresh log file for failed test cases
with open("failed_cases.txt", "w", encoding="utf-8") as f:
    f.write("WikiSQL Failed Cases\n")
    f.write("=" * 80 + "\n\n")

# Create the evaluation suite
db, tests = create_duckdb_eval_suite(sample_size=50)

print("\n========== Text2SQL Evaluation ==========\n")

correct = 0
total = len(tests)

# Evaluate each test case
for i, test in enumerate(tests, start=1):

    print("=" * 70)
    print(f"Test Case {i}")

    print("\nQuestion:")
    print(test["question"])

    print("\nTable:")
    print(test["table_name"])

    print("\nSchema:")
    print(json.dumps(test["schema_dict"], indent=2))

    # Generate SQL using the LLM
    generated_sql = generate_sql(
        test["question"],
        test["table_name"],
        test["schema_text"]
    )

    print("\nGenerated SQL:")
    print(generated_sql)

    print("\nGround Truth SQL:")
    print(test["ground_truth_sql"])

    # Execute generated SQL
    try:
        llm_result = db.execute(generated_sql).fetchall()

    except Exception as e:
        llm_result = f"Execution Error: {e}"

    # Execute ground-truth SQL
    try:
        gt_result = db.execute(
            test["ground_truth_sql"]
        ).fetchall()

    except Exception as e:
        gt_result = f"Execution Error: {e}"

    print("\nLLM Result:")
    print(llm_result)

    print("\nGround Truth Result:")
    print(gt_result)

    # Compare the outputs
    if llm_result == gt_result:

        print("\n✅ MATCH")
        correct += 1

    else:

        print("\n❌ NOT MATCH")

        # Store failed cases for future debugging
        with open(
            "failed_cases.txt",
            "a",
            encoding="utf-8"
        ) as f:

            f.write("=" * 80 + "\n")
            f.write(f"Test Case : {i}\n\n")

            f.write("Question:\n")
            f.write(test["question"] + "\n\n")

            f.write("Table:\n")
            f.write(test["table_name"] + "\n\n")

            f.write("Schema:\n")
            f.write(test["schema_text"] + "\n")

            f.write("Generated SQL:\n")
            f.write(generated_sql + "\n\n")

            f.write("Ground Truth SQL:\n")
            f.write(test["ground_truth_sql"] + "\n\n")

            f.write("LLM Result:\n")
            f.write(str(llm_result) + "\n\n")

            f.write("Ground Truth Result:\n")
            f.write(str(gt_result) + "\n\n")

# ============================================================
# Evaluation Summary
# ============================================================

print("\n" + "=" * 70)
print("Evaluation Summary")
print("=" * 70)

print(f"Total Test Cases : {total}")
print(f"Matched          : {correct}")
print(f"Not Matched      : {total - correct}")
print(f"Accuracy         : {(correct / total) * 100:.2f}%")

print("\n✅ Evaluation Completed.")