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

            tools = await session.list_tools()

            print(tools)

asyncio.run(main())