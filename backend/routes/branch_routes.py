from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from ..dependencies import SessionLocal
from ..models.branch_model import Branch
from ..schemas.branch_schema import BranchCreate, BranchResponse
from ..services.utils import db_dependency,user_dependency
from ..services.auth_service import is_admin
from typing import List

router = APIRouter(prefix="/branches", tags=["Branches"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=BranchResponse,status_code=status.HTTP_201_CREATED)
def create_branch(branch_data: BranchCreate, db: db_dependency,user: user_dependency):
    if user.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='You are not admin')
    existing_branch = db.query(Branch).filter(Branch.name == branch_data.name).first()
    if existing_branch:
        raise HTTPException(status_code=400, detail="Відділення з такою назвою вже існує")

    new_branch = Branch(**branch_data.dict())
    db.add(new_branch)
    db.commit()
    db.refresh(new_branch)
    return new_branch

@router.get("/", response_model=List[BranchResponse],status_code=status.HTTP_200_OK)
def get_branches(db: db_dependency):
    return db.query(Branch).all()

@router.get("/{branch_id}", response_model=BranchResponse,status_code=status.HTTP_200_OK)
def get_branch(branch_id: int, db: db_dependency):
    branch = db.query(Branch).filter(Branch.id == branch_id).first()
    if not branch:
        raise HTTPException(status_code=404, detail="Відділення не знайдено")
    return branch

@router.put("/{branch_id}", response_model=BranchResponse,status_code=status.HTTP_200_OK)
def update_branch(branch_id: int, branch_data: BranchCreate, db: db_dependency,user:user_dependency):
    if user.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='You are not admin')
    branch = db.query(Branch).filter(Branch.id == branch_id).first()
    if not branch:
        raise HTTPException(status_code=404, detail="Відділення не знайдено")

    for key, value in branch_data.dict().items():
        setattr(branch, key, value)

    db.commit()
    db.refresh(branch)
    return branch

@router.delete("/{branch_id}")
def delete_branch(branch_id: int, db: db_dependency,user:user_dependency):
  print(user.get("role"))
  if user.get("role") != "admin":
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='You are not admin')
  branch = db.query(Branch).filter(Branch.id == branch_id).first()
  if not branch:
    raise HTTPException(status_code=404, detail="Відділення не знайдено")
  db.delete(branch)
  db.commit()
  return {"message": "Відділення успішно видалено"}
