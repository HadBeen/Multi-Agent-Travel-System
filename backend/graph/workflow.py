import os 
import certifi
from dotenv import load_dotenv
import psycopg
from psycopg.rows import dict_row
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.graph import StateGraph, START, END
from backend.graph.states import TravelState
from backend.graph.nodes import (
    AGENT_ORDER,
    flight_agent,
    hotel_agent,
    weather_agent,
    itinerary_agent,
    final_agent,
    supervisor_agent,
    guardrail_blocked_agent,
    budget_agent,
    human_approval_agent)

load_dotenv()

os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()

def get_database_url():
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise ValueError(
            "DATABASE_URL is missing. Please add your Render PostgreSQL External Database URL to .env"
        )

    if "sslmode=" not in database_url:
        separator = "&" if "?" in database_url else "?"
        database_url = f"{database_url}{separator}sslmode=require"

    return database_url

# PostgreSQL Checkpointer
DATABASE_URL = get_database_url()
_conn = psycopg.connect(
DATABASE_URL,
autocommit=True,
row_factory=dict_row)
checkpointer = PostgresSaver(_conn)
checkpointer.setup()


# =========================
# Dynamic Supervisor Routing
# =========================
ROUTE_MAP = {
    "guardrail_blocked": "guardrail_blocked",
    "flight_agent": "flight_agent",
    "hotel_agent": "hotel_agent",
    "weather_agent": "weather_agent",
    "budget_agent": "budget_agent",
    "itinerary_agent": "itinerary_agent",
}


def _selected_agents(state: TravelState) -> list[str]:
    selected = state.get("selected_agents", [])
    return [agent for agent in AGENT_ORDER if agent in selected]


def route_from_supervisor(state: TravelState) -> str:
    if not state.get("guardrail_allowed", True):
        return "guardrail_blocked"

    selected = _selected_agents(state)
    return selected[0] if selected else "itinerary_agent"


def route_after_agent(current_agent: str):
    def route(state: TravelState) -> str:
        selected = _selected_agents(state)
        current_index = AGENT_ORDER.index(current_agent)

        for next_agent in AGENT_ORDER[current_index + 1 :]:
            if next_agent in selected:
                return next_agent

        return "itinerary_agent"

    return route


def create_graph():

    graph = StateGraph(TravelState)
    graph.add_node("supervisor", supervisor_agent)
    graph.add_node("guardrail_blocked", guardrail_blocked_agent)
    graph.add_node("flight_agent", flight_agent)
    graph.add_node("hotel_agent", hotel_agent)
    graph.add_node("weather_agent", weather_agent)
    graph.add_node("budget_agent", budget_agent)
    graph.add_node("itinerary_agent", itinerary_agent)
    graph.add_node("human_approval", human_approval_agent)
    graph.add_node("final_agent", final_agent)

    graph.add_edge(START, "supervisor")
    graph.add_conditional_edges("supervisor", route_from_supervisor, ROUTE_MAP)

    graph.add_conditional_edges(
        "flight_agent", route_after_agent("flight_agent"), ROUTE_MAP
    )
    graph.add_conditional_edges(
        "hotel_agent", route_after_agent("hotel_agent"), ROUTE_MAP
    )
    graph.add_conditional_edges(
        "weather_agent", route_after_agent("weather_agent"), ROUTE_MAP
    )
    graph.add_conditional_edges("budget_agent", route_after_agent("budget_agent"), ROUTE_MAP
    )

    graph.add_edge("itinerary_agent", "human_approval")
    graph.add_edge("human_approval", "final_agent")
    graph.add_edge("final_agent", END)
    graph.add_edge("guardrail_blocked", END)

    
    app = graph.compile(checkpointer=checkpointer)
    return app



app = create_graph()
