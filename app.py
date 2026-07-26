import asyncio

from llm import generate_sql
from validator import validate_sql

from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters


DB_PATH = "data/company.duckdb"


async def main():

    question = input("Ask your question: ")

    sql = generate_sql(question)

    print("\nGenerated SQL:\n")
    print(sql)

    if not validate_sql(sql):
        print("\nSQL Validation Failed")
        return

    server = StdioServerParameters(
        command="python",
        args=[
            "-m",
            "uv",
            "tool",
            "run",
            "mcp-server-duckdb",
            "--db-path",
            DB_PATH
        ]
    )

    async with stdio_client(server) as (read, write):

        async with ClientSession(read, write) as session:

            await session.initialize()

            result = await session.call_tool(
                "query",
                {
                    "query": sql
                }
            )

            print("\nResult:\n")

            for item in result.content:
                print(item.text)


if __name__ == "__main__":
    asyncio.run(main())