# backend/app/agents/graph/state.py

from typing import TypedDict, List, Dict, Any, Optional


class PlanStep(TypedDict):
    name: str
    description: str
    tool: Optional[str]


class PlannerOutput(TypedDict):
    steps: List[PlanStep]
    needs_internal_research: bool
    needs_external_research: bool
    confidence_threshold: float


class ResearchResult(TypedDict):
    source: str              # "vector_db" | "web"
    content: str
    metadata: Dict[str, Any]


class AnalysisResult(TypedDict):
    insights: List[str]
    gaps: List[str]
    confidence: float


class AgentState(TypedDict):
    # ---- Identity & Context ----
    user_id: str
    project_id: str
    goal: str

    # ---- Planner ----
    plan: Optional[PlannerOutput]

    # ---- Research ----
    internal_research: List[ResearchResult]
    external_research: List[ResearchResult]

    # ---- Analysis ----
    analysis: Optional[AnalysisResult]

    # ---- Final Output ----
    final_output: Optional[str]

    # ---- Execution Metadata ----
    errors: List[str]
