# Multi-Agent Stock Analysis Dashboard 📈🤖

An intelligent, multi-agent AI system designed to perform comprehensive stock analysis. This project leverages an architecture of specialized AI agents to evaluate financial data, summarize market sentiment, and provide actionable investment insights through an interactive dashboard.

## 🚀 Overview

This repository provides an end-to-end AI engineering solution for financial analysis. By utilizing a stateful, graph-based approach, it orchestrates multiple AI agents—each with distinct roles (e.g., technical analysis, fundamental analysis, news sentiment)—to collaborate on evaluating specific equities and generating synthesized reports.

## 🏗️ Architecture & Core Components

- **State Management (`state.py`)**: Defines the shared state passed between agents, ensuring context and memory are maintained throughout the analysis pipeline.
- **Graph Builder (`graph_builder.py`)**: Constructs the execution flow of the agents. It defines the nodes (agents) and edges (conditional routing), orchestrating the multi-agent workflow seamlessly.
- **Specialized Agents (`agents/`)**: Contains the prompts, behavior, and logic for individual AI personas, allowing for a modular and scalable system.
- **Tools (`tools/`)**: Custom tool integrations enabling the agents to interact with external environments, such as fetching real-time market data, financial statements, or executing web searches.
- **Core Engine (`stock_analyzer.py` & `main.py`)**: The backend engine that initializes the graph state and triggers the analysis process.
- **User Interface (`frontend.py`)**: An interactive web-based dashboard designed to visualize the agentic workflow and present the final stock reports to the user.

## 💻 Tech Stack

- **Language:** Python
- **AI/LLM Framework:** LangGraph (for agent orchestration and graph building)
- **Frontend UI:** Streamlit / Flask 
- **Data Integration:** Financial data APIs (e.g., yfinance) and custom search tools

## 📂 Repository Structure

```text
multi-agent-stock-analysis-dashboard/
├── agents/                 # Logic and instructions for specialized AI agents
├── tools/                  # Custom tools for data retrieval and processing
├── .gitignore              # Git ignore configurations
├── frontend.py             # Web dashboard UI implementation
├── graph_builder.py        # Multi-agent graph construction and routing logic
├── main.py                 # Application entry point for backend execution
├── requirements.txt        # Python dependencies
├── state.py                # State definitions for agent memory and tracking
└── stock_analyzer.py       # Core evaluation and synthesis logic
