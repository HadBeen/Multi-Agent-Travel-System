from backend.mcp_client.client import Client

search_tool = None

async def initialize_mcp():
    """
    Initialize only Tavily.

    Previously this function initialized all MCP servers,
    so an AviationStack or Weather failure also caused
    Tavily hotel search to fail.
    """

    global search_tool

    if search_tool is not None:
        return

    tools = await Client.get_tools(
        server_name="tavily"
    )

    tools_by_name = {
        tool.name: tool
        for tool in tools
    }

    search_tool = tools_by_name.get(
        "tavily_search"
    )

    if search_tool is None:
        available_tools = ", ".join(
            tools_by_name.keys()
        )

        raise RuntimeError(
            "Tavily MCP connected, but the "
            "'tavily_search' tool was not found. "
            f"Available tools: "
            f"{available_tools or 'none'}"
        )

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
    await initialize_mcp()

    result = await search_tool.ainvoke(
        {
            "query": query
        }
    )

    return result