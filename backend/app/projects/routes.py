from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.db.database import SessionLocal
from app.db.models import Project, User
from .schemas import CreateProjectRequest

router = APIRouter(prefix="/projects")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_project(
    data: CreateProjectRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    name = data.name
    description = data.description
    project = Project(
        name=name,
        description=description,
        user_id=user.id
    )
    db.add(project)
    db.commit()
    db.refresh(project)

    return project


@router.get("/")
def list_projects(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    projects = db.query(Project).filter(Project.user_id == user.id).all()
    return projects
