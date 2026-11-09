from backend.mcp_client.client import Client 

aviation_tools = {}



async def initialize_aviation_tools():
    print("\nINITIALIZING AVIATION TOOLS\n")
    global aviation_tools

    if aviation_tools:
        return

  
    try:
        # print({name: cfg.get("transport") for name, cfg in Client.connections.items()})
        tools = await Client.get_tools(server_name="Aviationstack MCP")
    except BaseException as e:
        print("AVIATION INIT FAILED:", type(e).__name__, e)
        raise

    aviation_tools = {
        tool.name: tool
        for tool in tools
    }

    if not aviation_tools:
        raise RuntimeError(
            "AviationStack MCP connected but "
            "returned no tools."
        )


async def aviation_mcp_call(tool_name: str,tool_args: dict = None):
    
    await initialize_aviation_tools()

    tool = aviation_tools.get(tool_name)

    if tool is None:
        available_tools = ", ".join(
            sorted(aviation_tools.keys())
        )

        raise ValueError(
            f"AviationStack tool '{tool_name}' "
            "was not found. "
            f"Available tools: "
            f"{available_tools or 'none'}"
        )

    result = await tool.ainvoke(
        tool_args or {}
    )

    return result

