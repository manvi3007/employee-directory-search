
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models.employee import Employee

MAX_RESULTS = 50


def search_employees(db: Session, search: str) -> list[Employee]:
    statement = select(Employee)

    if search:
        
        escaped_search = (
            search.replace("\\", "\\\\")
            .replace("%", "\\%")
            .replace("_", "\\_")
        )
        pattern = f"{escaped_search}%"

        statement = statement.where(
            or_(
                Employee.name.like(pattern, escape="\\"),
                Employee.department.like(pattern, escape="\\"),
            )
        )

    statement = statement.order_by(Employee.id).limit(MAX_RESULTS)

    return list(db.scalars(statement).all())
