# event loop
import os
import asyncio
from dotenv import load_dotenv
import certifi
from langchain_mcp_adapters.client import MultiServerMCPClient

os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

Client = MultiServerMCPClient(
    {
        "tavily":{
                    "transport": "streamable_http",
                    "url": f"https://mcp.tavily.com/mcp/?tavilyApiKey={TAVILY_API_KEY}"
                },
    }
)
tavily_search_tool = None

async def get_tavily_tools():
    tools = await Client.get_tools()
    for tool in tools : 
        print(tool.name)



async def get_tavily_search_tool():
    global tavily_search_tool
    
    if tavily_search_tool is None:
        tools = await Client.get_tools()
        tavily_search_tool = next(
            tool
            for tool in tools
            if tool.name == "tavily_search"
        )
    return tavily_search_tool


async def tavily_mcp_search(query: str):
    await get_tavily_search_tool()
    result = await tavily_search_tool.ainvoke({"query": query})
    return result

asyncio.run(tavily_mcp_search("Best hotels in New York City"))