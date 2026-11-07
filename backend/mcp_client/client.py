import os
from dotenv import load_dotenv
import certifi
from langchain_mcp_adapters.client import MultiServerMCPClient

os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
AVIATIONSTACK_API_KEY = os.getenv("AVIATIONSTACK_API_KEY")


Client = MultiServerMCPClient(
    {
        "tavily":
                {
                    "transport": "streamable_http",
                    "url": f"https://mcp.tavily.com/mcp/?tavilyApiKey={TAVILY_API_KEY}"
                },
        "Aviationstack MCP":
                {         
                    "transport":"stdio",
                    "command": "uvx",
                    "args": ["aviationstack-mcp"],
                    "env": {f"AVIATION_STACK_API_KEY": "{AVIATIONSTACK_API_KEY}"}
                }
    }
)


async def get_all_tools():
    tools = await Client.get_tools()
    return tools