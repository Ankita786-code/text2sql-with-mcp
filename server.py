from mcp.server.fastmcp import FastMCP
import duckdb

mcp = FastMCP("DuckDB Server")

con = duckdb.connect("student.db")

@mcp.tool()
def run_query(sql: str):
    return con.execute(sql).fetchall()

if __name__ == "__main__":
    mcp.run()