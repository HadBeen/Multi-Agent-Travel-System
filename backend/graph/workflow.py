from langgraph.graph import StateGraph, START, END
from graph.states import TravelState
from graph.nodes import (
    flight_agent,
    hotel_agent,
    itinerary_agent,
    final_agent)


def create_graph():
    
    graph = StateGraph(TravelState)

    graph.add_node("flight_agent", flight_agent)
    graph.add_node("hotel_agent", hotel_agent)
    graph.add_node("itinerary_agent", itinerary_agent)
    graph.add_node("final_agent", final_agent)

    graph.add_edge(START, "flight_agent")
    graph.add_edge("flight_agent", "hotel_agent")
    graph.add_edge("hotel_agent", "itinerary_agent")
    graph.add_edge("itinerary_agent", "final_agent")
    graph.add_edge("final_agent", END)
    
    app = graph.compile()
    return app



app = create_graph()
