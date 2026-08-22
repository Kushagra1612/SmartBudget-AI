"""
Tests on the LangGraph structure itself (app/ai/graph.py), separate from
the /ai/* endpoint tests in test_ai_api.py. These check the graph is
actually what it claims to be.
"""

from langgraph.graph.state import CompiledStateGraph

from app.ai.graph import ALL_AGENTS, financial_graph


def test_financial_graph_is_a_compiled_langgraph_state_graph():
    assert isinstance(financial_graph, CompiledStateGraph)


def test_graph_has_the_coordinator_and_all_four_agent_nodes():
    node_names = set(financial_graph.get_graph().nodes.keys())

    assert "coordinator" in node_names
    assert "responder" in node_names

    for agent in ALL_AGENTS:
        assert f"{agent}_agent" in node_names


def test_all_four_agent_nodes_are_reachable_from_the_coordinator():
    graph_repr = financial_graph.get_graph()
    edges_from_coordinator = {
        edge.target for edge in graph_repr.edges if edge.source == "coordinator"
    }

    for agent in ALL_AGENTS:
        assert f"{agent}_agent" in edges_from_coordinator


def test_every_agent_node_feeds_into_the_responder():
    graph_repr = financial_graph.get_graph()

    for agent in ALL_AGENTS:
        node = f"{agent}_agent"
        targets = {
            edge.target for edge in graph_repr.edges if edge.source == node
        }
        assert "responder" in targets
