from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.auth.dependencies import get_current_user
from app.agents.run import run_agent
from app.db.models import User

router = APIRouter(prefix="/agent")


class AgentRunRequest(BaseModel):
    project_id: str
    goal: str


@router.post("/run")
def run_agent_endpoint(
    data: AgentRunRequest,
    current_user: User = Depends(get_current_user)
):
    result = run_agent(
        user_id=str(current_user.id),
        project_id=data.project_id,
        goal=data.goal
    )
    
    return {
        "final_output": result.get("final_output"),
        "status": "completed" if result.get("final_output") else "error"
    }

