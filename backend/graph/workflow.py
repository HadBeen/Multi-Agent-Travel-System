import os 
import certifi
from dotenv import load_dotenv
import psycopg
from psycopg.rows import dict_row
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.graph import StateGraph, START, END
from backend.graph.states import TravelState
from backend.graph.nodes import (
    flight_agent,
    hotel_agent,
    weather_agent,
    itinerary_agent,
    final_agent)

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

def create_graph():

    graph = StateGraph(TravelState)
    
    graph.add_node("flight_agent", flight_agent)
    graph.add_node("hotel_agent", hotel_agent)
    graph.add_node("weather_agent", weather_agent)
    graph.add_node("itinerary_agent", itinerary_agent)
    graph.add_node("final_agent", final_agent)

    graph.add_edge(START, "flight_agent")
    graph.add_edge("flight_agent", "hotel_agent")
    graph.add_edge("hotel_agent", "weather_agent")
    graph.add_edge("weather_agent", "itinerary_agent")
    graph.add_edge("itinerary_agent", "final_agent")
    graph.add_edge("final_agent", END)

    
    app = graph.compile(checkpointer=checkpointer)
    return app



app = create_graph()
