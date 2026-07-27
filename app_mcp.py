from llm import generate_sql
from validator import validate_sql
from schema import get_schema
from mcp_client import execute_sql


def main():

    question = input("Ask your question: ")

    # Get database schema
    schema = get_schema()

    # Generate SQL using LLM
    sql = generate_sql(question, schema)

    print("\nGenerated SQL:\n")
    print(sql)

    # Validate SQL
    if not validate_sql(sql):
        print("\nSQL Validation Failed")
        return

    print("\nExecuting through MCP...\n")

    try:
        result = execute_sql(sql)

        print("Result:\n")

        if isinstance(result, list):
            for row in result:
                print(row)
        else:
            print(result)

    except Exception as e:
        print("\nExecution Error:")
        print(e)


if __name__ == "__main__":
    main()