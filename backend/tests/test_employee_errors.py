
from unittest.mock import patch

from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError

from app.database import get_db
from app.main import app


def override_get_db():
    yield object()


def test_database_error_returns_503():
    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(
            app,
            raise_server_exceptions=False,
        ) as client:
            with patch(
                "app.services.employee_service.search_employees",
                side_effect=SQLAlchemyError("database unavailable"),
            ):
                response = client.get(
                    "/employees",
                    params={"search": "rahul"},
                )

        assert response.status_code == 503
        assert "temporarily unavailable" in (
            response.json()["detail"].lower()
        )
    finally:
        app.dependency_overrides.clear()
