import os
import sys
from dotenv import load_dotenv
import certifi
from pathlib import Path
from langchain_mcp_adapters.client import MultiServerMCPClient

os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
AVIATIONSTACK_API_KEY = os.getenv("AVIATIONSTACK_API_KEY")
AVIATION_ENV = os.environ.copy()
AVIATION_ENV["AVIATION_STACK_API_KEY"] = (AVIATIONSTACK_API_KEY)

BASE_DIR = Path(__file__).resolve().parents[2]   # multi-agent-system (client.py is in backend/mcp_client/)
WEATHER_SERVER_PATH = BASE_DIR / "mcp_servers" / "weather_custom_mcp.py"

Client = MultiServerMCPClient(
    {
        "tavily":
                {
                    "transport": "streamable_http",
                    "url": f"https://mcp.tavily.com/mcp/?tavilyApiKey={TAVILY_API_KEY}"
                },
        # "Aviationstack MCP":
        #         {   
        #             "transport": "stdio",
        #             "command": "uvx",
        #             "args": ["aviationstack-mcp"],
        #                   "env": {"AVIATION_STACK_API_KEY": f"{AVIATIONSTACK_API_KEY}" }
        #         },
        "weather": 
                {
                    "transport": "stdio",
                    # Use the same Python environment that runs app.py.
                    "command": sys.executable,
                    "args": [str(WEATHER_SERVER_PATH)],
                }
    }
)

def leaf_errors(e):
    if isinstance(e, BaseExceptionGroup):
        for sub in e.exceptions:
            yield from leaf_errors(sub)
    else:
        yield e

async def get_all_tools():
    """
    Load each MCP server separately.

    A broken server will no longer prevent the other
    working servers from loading.
    """
    all_tools = []
    print(WEATHER_SERVER_PATH)
    for server_name in (
        "tavily",
        "Aviationstack MCP",
        "weather"
    ):
        try:
            tools = await Client.get_tools(
                server_name=server_name
            )

            all_tools.extend(tools)

            print(
                f"\nAvailable tools from "
                f"{server_name} MCP:\n"
            )

            for tool in tools:
                print(tool.name)

        except BaseException as error:
            print(f"\nCould not connect to {server_name} MCP:")
            for leaf in leaf_errors(error):
                print("  LEAF:", type(leaf).__name__, "-", leaf)

    return all_tools


