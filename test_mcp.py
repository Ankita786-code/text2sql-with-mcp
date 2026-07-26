import asyncio

from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters


async def main():

    server = StdioServerParameters(
        command="python",
        args=[
            "-m",
            "uv",
            "tool",
            "run",
            "mcp-server-duckdb",
            "--db-path",
            "data/company.duckdb",
        ],
    )

    async with stdio_client(server) as (read_stream, write_stream):

        async with ClientSession(read_stream, write_stream) as session:

            await session.initialize()

            result = await session.call_tool(
                "query",
                {
                    "query": "SELECT 1;"
                }
            )

            print("TYPE:")
            print(type(result))

            print("\nRESULT:")
            print(result)

            print("\nDICT:")
            print(result.__dict__)


asyncio.run(main())