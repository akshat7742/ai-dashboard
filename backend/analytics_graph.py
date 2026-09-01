from langgraph.graph import (
    StateGraph,
    START,
    END
)

from langgraph.checkpoint.memory import MemorySaver

from langchain_core.messages import SystemMessage

from langgraph.prebuilt import ToolNode

from llm import chat_model

from tools import create_analytics_tools

from agent_state import AgentState


SYSTEM_PROMPT = """
You are an AI Business Analytics Agent.

You analyze a business dashboard and answer questions
using the available analytics tools.

Available tools:

1. get_dashboard_summary

   Use for:

   - overall dashboard summaries
   - key insights
   - main issues
   - recommendations
   - high-level dashboard analysis


2. get_kpi_analysis

   Use for:

   - sales
   - revenue
   - orders
   - customers
   - KPI questions


3. get_trend_analysis

   Use for:

   - sales trends
   - growth
   - increases
   - decreases
   - monthly performance


4. get_region_analysis

   Use for:

   - regional performance
   - best region
   - worst region
   - region comparisons


Rules:

1. Use dashboard tools whenever numerical
   dashboard information is required.

2. Never invent dashboard numbers.

3. Use multiple tools when the question requires
   multiple types of analysis.

4. Compare actual values before making conclusions.

5. Clearly distinguish between:

   - facts from the dashboard
   - analytical conclusions
   - recommendations

6. Keep the answer concise.

7. When appropriate, structure the answer as:

   Insight:
   Evidence:
   Recommendation:

8. If the user asks for an overall dashboard analysis,
   use get_dashboard_summary first.

9. Use the previous conversation context when
   answering follow-up questions.

10. If the user asks questions such as:

   - why?
   - why is that?
   - what about it?
   - compare it with South
   - how does it perform?
   - what about the other region?

   use the previous conversation to understand
   what the user is referring to.

11. Do not ask the user to repeat information that
    already exists in the conversation.
"""


def create_analytics_graph(dashboard_data):

    # --------------------------------------------------
    # Create analytics tools
    # --------------------------------------------------

    tools = create_analytics_tools(
        dashboard_data
    )

    # --------------------------------------------------
    # Connect tools to LLM
    # --------------------------------------------------

    llm_with_tools = chat_model.bind_tools(
        tools
    )

    # --------------------------------------------------
    # Agent node
    # --------------------------------------------------

    def agent_node(state: AgentState):

        messages = state["messages"]

        response = llm_with_tools.invoke(
            [
                SystemMessage(
                    content=SYSTEM_PROMPT
                ),
                *messages
            ]
        )

        return {
            "messages": [response]
        }

    # --------------------------------------------------
    # Tool node
    # --------------------------------------------------

    tool_node = ToolNode(tools)

    # --------------------------------------------------
    # Decide whether to call a tool
    # --------------------------------------------------

    def should_continue(state: AgentState):

        last_message = state["messages"][-1]

        tool_calls = getattr(
            last_message,
            "tool_calls",
            None
        )

        if tool_calls:
            return "tools"

        return END

    # --------------------------------------------------
    # Create graph
    # --------------------------------------------------

    graph = StateGraph(
        AgentState
    )

    # --------------------------------------------------
    # Add nodes
    # --------------------------------------------------

    graph.add_node(
        "agent",
        agent_node
    )

    graph.add_node(
        "tools",
        tool_node
    )

    # --------------------------------------------------
    # Start → Agent
    # --------------------------------------------------

    graph.add_edge(
        START,
        "agent"
    )

    # --------------------------------------------------
    # Agent → Tools OR END
    # --------------------------------------------------

    graph.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            END: END
        }
    )

    # --------------------------------------------------
    # Tools → Agent
    # --------------------------------------------------

    graph.add_edge(
        "tools",
        "agent"
    )

    # --------------------------------------------------
    # Conversation memory
    # --------------------------------------------------

    memory = MemorySaver()

    # --------------------------------------------------
    # Compile graph with memory
    # --------------------------------------------------

    return graph.compile(
        checkpointer=memory
    )