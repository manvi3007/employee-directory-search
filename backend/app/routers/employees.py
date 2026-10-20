
import logging

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.employee import EmployeeResponse
from app.services.employee_service import find_employees

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/employees", tags=["Employees"])


@router.get("", response_model=list[EmployeeResponse])
def get_employees(
    search: str = Query(default="", max_length=100),
    db: Session = Depends(get_db),
):
    try:
        return find_employees(db, search)
    except SQLAlchemyError:
        logger.exception("Database error while searching employees")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Employee search is temporarily unavailable. Please try again.",
        ) from None
