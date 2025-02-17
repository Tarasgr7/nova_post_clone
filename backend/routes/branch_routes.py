from fastapi import APIRouter, HTTPException,status
from ..dependencies import logger
from ..models.branch_model import Branch
from ..schemas.branch_schema import BranchCreate
from ..services.utils import db_dependency,user_dependency,check_admin_role
from ..services.auth_service import is_admin


router = APIRouter(prefix="/branches", tags=["Branches"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_branch(branch_data: BranchCreate, db: db_dependency, user: user_dependency):
    check_admin_role(user)

    # Перевірка на існування відділення з таким ім'ям
    existing_branch = db.query(Branch).filter(Branch.name == branch_data.name).first()
    if existing_branch:
        logger.warning(f"Спроба створення відділення з існуючою назвою: {branch_data.name}")
        raise HTTPException(status_code=400, detail="Відділення з такою назвою вже існує")

    # Створення нового відділення
    new_branch = Branch(**branch_data.dict())
    db.add(new_branch)
    db.commit()
    db.refresh(new_branch)

    logger.info(f"Нове відділення створене: {new_branch.name} з ID: {new_branch.id}")
    return new_branch

@router.get("/", status_code=status.HTTP_200_OK)
def get_branches(db: db_dependency):
    branches = db.query(Branch).all()
    logger.info(f"Отримано список всіх відділень: знайдено {len(branches)} відділень.")
    return branches

@router.get("/{branch_id}", status_code=status.HTTP_200_OK)
def get_branch(branch_id: int, db: db_dependency):
    branch = db.query(Branch).filter(Branch.id == branch_id).first()
    if not branch:
        logger.warning(f"Відділення з ID: {branch_id} не знайдено.")
        raise HTTPException(status_code=404, detail="Відділення не знайдено")
    
    logger.info(f"Відділення з ID: {branch_id} отримано.")
    return branch

@router.put("/{branch_id}", status_code=status.HTTP_200_OK)
def update_branch(branch_id: int, branch_data: BranchCreate, db: db_dependency, user: user_dependency):
    check_admin_role(user)

    branch = db.query(Branch).filter(Branch.id == branch_id).first()
    if not branch:
        logger.warning(f"Відділення з ID: {branch_id} не знайдено для оновлення.")
        raise HTTPException(status_code=404, detail="Відділення не знайдено")

    # Оновлення полів відділення
    for key, value in branch_data.dict().items():
        setattr(branch, key, value)

    db.commit()
    db.refresh(branch)

    logger.info(f"Відділення з ID: {branch_id} успішно оновлено.")
    return branch

@router.delete("/{branch_id}",status_code=status.HTTP_200_OK)
def delete_branch(branch_id: int, db: db_dependency, user: user_dependency):
    check_admin_role(user)

    branch = db.query(Branch).filter(Branch.id == branch_id).first()
    if not branch:
        logger.warning(f"Відділення з ID: {branch_id} не знайдено для видалення.")
        raise HTTPException(status_code=404, detail="Відділення не знайдено")

    db.delete(branch)
    db.commit()

    logger.info(f"Відділення з ID: {branch_id} успішно видалено.")
    return {"message": "Відділення успішно видалено"}