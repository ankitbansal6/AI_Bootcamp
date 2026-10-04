import asyncio
from fastmcp import Client

async def main() -> None:
    # Connect to a local server script via STDIO, or use a URL like "https://api.example.com/mcp"
    async with Client("http://127.0.0.1:8000/mcp") as client:
    #async with Client("mcpserver.py") as client:
        # List available tools on the server
        tools = await client.list_tools()
        # for tool in tools:
        #     print(tool.name)
        #     print(tool.input_schema)
        #     print(tool.description)

        
        #Call a specific tool with arguments
        result = await client.call_tool(
            name="get_stock_details",
            arguments={"stock_code": "INFY"}
        )
        print("Tool result:", result)

if __name__ == "__main__":
    asyncio.run(main())
