from langgraph.graph import StateGraph
from typing import TypedDict

from app.services.ai_service import (
    extract_cv,
    extract_job,
    compare_and_generate,
    rewrite_cv,
    generate_roadmap
)


class AgentState(TypedDict):
    cv_text: str
    job_text: str
    cv_data: dict
    job_data: dict
    analysis: dict
    rewritten_cv: dict
    roadmap: dict


def extract_cv_node(state: AgentState):
    state["cv_data"] = extract_cv(state["cv_text"])
    return state


def extract_job_node(state: AgentState):
    state["job_data"] = extract_job(state["job_text"])
    return state


def compare_node(state: AgentState):
    state["analysis"] = compare_and_generate(
        state["cv_data"], state["job_data"]
    )
    return state


def rewrite_node(state: AgentState):
    state["rewritten_cv"] = rewrite_cv(
        state["cv_text"],
        state["job_text"],
        state["analysis"]
    )
    return state


def roadmap_node(state: AgentState):
    state["roadmap"] = generate_roadmap(state["analysis"])
    return state

def build_agent():
    graph = StateGraph(AgentState)

    graph.add_node("extract_cv", extract_cv_node)
    graph.add_node("extract_job", extract_job_node)
    graph.add_node("compare", compare_node)
    graph.add_node("rewrite", rewrite_node)
    graph.add_node("roadmap", roadmap_node)

    graph.set_entry_point("extract_cv")

    graph.add_edge("extract_cv", "extract_job")
    graph.add_edge("extract_job", "compare")

    # 🔥 AQUÍ ESTÁ LA MAGIA
    graph.add_conditional_edges(
        "compare",
        decide_next_step,
        {
            "rewrite": "rewrite",
            "roadmap": "roadmap",
            "end": "__end__"
        }
    )

    # flujo después de rewrite
    graph.add_edge("rewrite", "roadmap")

    return graph.compile()

def decide_next_step(state: AgentState) -> str:
    analysis = state.get("analysis", {})
    score = analysis.get("match_score", 0)

    if score < 60:
        return "rewrite"
    elif score < 80:
        return "roadmap"
    else:
        return "end"