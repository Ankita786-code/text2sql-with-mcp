import asyncio
import ast

from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters


class MCPClient:

    def __init__(self):

        self.server = StdioServerParameters(
            command="python",
            args=[
                "-m",
                "uv",
                "tool",
                "run",
                "mcp-server-duckdb",
                "--db-path",
                "data/company.duckdb"
            ]
        )

    async def execute(self, sql):

        async with stdio_client(self.server) as (read, write):

            async with ClientSession(read, write) as session:

                await session.initialize()

                result = await session.call_tool(
                    "query",
                    {
                        "query": sql
                    }
                )

                text = result.content[0].text

                try:
                    return ast.literal_eval(text)
                except:
                    return text


_client = MCPClient()


def execute_sql(sql):

    return asyncio.run(
        _client.execute(sql)
    )