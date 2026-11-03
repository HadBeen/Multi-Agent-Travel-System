

# Multi-Agent Travel Planner

An AI-powered travel planning assistant built with **LangGraph and MCP**, leveraging a team of specialized AI agents to generate personalized travel itineraries, retrieve travel information, and estimate trip budgets.

A Supervisor Agent dynamically coordinates the agents, while guardrails and Human-in-the-Loop mechanisms ensure controlled and reliable execution.

## Key Features

- **Multi-Agent Architecture:** Specialized agents for flights, hotels, weather, budgeting, and itinerary generation.
- **Supervisor Agent:** Dynamically orchestrates agents and manages workflow execution.
- **MCP Integration:** Connects AI agents to external tools and APIs through the Model Context Protocol.
- **AI Guardrails:** Validates user requests and helps prevent unsafe or irrelevant interactions.
- **Human-in-the-Loop:** Allows users to review and approve generated itineraries.
- **Persistent Memory:** Maintains workflow state and conversation context.
- **Observability:** Tracks agent execution and LLM interactions through LangSmith.

## Tech Stack

| Category | Technologies |
|---|---|
| Language | Python |
| AI & LLMs | Groq, Llama 3, LangChain |
| Agent Orchestration | LangGraph |
| Tool Integration | MCP (Model Context Protocol) |
| External APIs | Tavily, AviationStack, OpenWeather |
| Backend | FastAPI |
| Frontend | HTML, CSS, JavaScript |
| Database | PostgreSQL |
| Monitoring | LangSmith |
| Deployment | Docker, Render |

##  Architecture

User Request → Guardrails → Supervisor Agent → Specialized Agents → MCP Tools → Itinerary Generation → Human Approval → Final Travel Plan
ent state management, and human oversight into a single end-to-end application.
