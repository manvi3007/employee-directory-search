
from unittest.mock import MagicMock

from app.repositories.employee_repository import search_employees


def run_search(search: str):
    db = MagicMock()
    db.scalars.return_value.all.return_value = []

    search_employees(db, search)

    statement = db.scalars.call_args.args[0]
    return statement


def test_search_uses_prefix_matching_and_limits_results():
    statement = run_search("rahul")

    sql = str(statement).lower()
    params = statement.compile().params

    assert "employees.name like" in sql
    assert "employees.department like" in sql
    assert "limit" in sql
    assert "where" in sql
    assert "rahul%" in params.values()
    assert not any(value == "%rahul%" for value in params.values())


def test_search_escapes_like_wildcards():
    statement = run_search("%ra_")

    params = statement.compile().params

    assert "\\%ra\\_%" in params.values()


def test_empty_search_still_limits_results():
    statement = run_search("")

    sql = str(statement).lower()

    assert "limit" in sql
    assert "where" not in sql
