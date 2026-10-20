
from sqlalchemy.orm import Session

from app.repositories.employee_repository import search_employees
from app.models.employee import Employee


def find_employees(db: Session, search: str) -> list[Employee]:
    normalized_search = search.strip()
    return search_employees(db, normalized_search)
