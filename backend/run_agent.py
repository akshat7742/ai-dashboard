from analytics_graph import create_analytics_graph


# This will hold the compiled graph.
# The graph is created once when the backend starts.
analytics_graph = None


def initialize_agent(dashboard_data):

    global analytics_graph

    analytics_graph = create_analytics_graph(
        dashboard_data
    )


def run_agent(
    question: str,
    conversation_id: str
):

    if analytics_graph is None:

        raise RuntimeError(
            "Analytics agent has not been initialized."
        )

    result = analytics_graph.invoke(

        {
            "messages": [
                {
                    "role": "user",
                    "content": question
                }
            ]
        },

        config={
            "configurable": {
                "thread_id": conversation_id
            }
        }
    )

    return result[
        "messages"
    ][-1].content