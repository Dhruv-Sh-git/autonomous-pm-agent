import time
import mlflow

from app.agents.graph.graph import build_agent_graph
from app.agents.graph.state import AgentState

graph = build_agent_graph()

# Optional but recommended (set once)
mlflow.set_experiment("APMA-Agent-Runs")


def run_agent(
    user_id: str,
    project_id: str,
    goal: str
) -> AgentState:
    start_time = time.time()

    initial_state: AgentState = {
        "user_id": user_id,
        "project_id": project_id,
        "goal": goal,
        "plan": None,
        "internal_research": [],
        "external_research": [],
        "analysis": None,
        "final_output": None,
        "errors": [],
        "analysis_iterations": 0,
    }

    with mlflow.start_run():
        # ---- PARAMS ----
        mlflow.log_param("user_id", user_id)
        mlflow.log_param("project_id", project_id)
        mlflow.log_param("goal", goal)

        # ---- EXECUTION ----
        final_state: AgentState = graph.invoke(initial_state)

        # ---- METRICS ----
        latency = time.time() - start_time
        mlflow.log_metric("latency_sec", latency)
        mlflow.log_metric(
            "analysis_iterations",
            final_state.get("analysis_iterations", 0)
        )
        mlflow.log_metric(
            "error_count",
            len(final_state.get("errors", []))
        )

        # ---- ARTIFACTS ----
        if final_state.get("final_output"):
            mlflow.log_text(
                final_state["final_output"],
                "final_output.md"
            )

        if final_state.get("analysis"):
            mlflow.log_text(
                str(final_state["analysis"]),
                "analysis.txt"
            )

        return final_state
