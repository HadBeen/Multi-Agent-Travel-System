from backend.mcp_client.client import Client

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