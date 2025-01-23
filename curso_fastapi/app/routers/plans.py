from fastapi import APIRouter
from models import Plan, Customer
from db import SessionDep
from sqlmodel import select
router = APIRouter()

@router.post("/plans", response_model=Plan, tags=["Plans"])
async def create_plan(plan_data: Plan, session: SessionDep):
    plan_db = Plan.model_validate(plan_data.model_dump())
    session.add(plan_db)
    session.commit()
    session.refresh(plan_db)
    return plan_db
    
    
@router.get("/plans", response_model=list[Plan], tags=["Plans"])
async def list_plans(session: SessionDep):
    return session.exec(select(Plan)).all()
    
    