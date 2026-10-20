
from datetime import date
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.database import get_db
from app.main import app


class FakeEmployee:
    def __init__(
        self,
        id,
        name,
        email,
        department,
        designation,
        date_of_joining,
    ):
        self.id = id
        self.name = name
        self.email = email
        self.department = department
        self.designation = designation
        self.date_of_joining = date_of_joining


def override_get_db():
    yield object()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def make_employee():
    return FakeEmployee(
        1,
        "Rahul Sharma",
        "rahul@company.com",
        "Engineering",
        "Software Engineer",
        date(2024, 1, 15),
    )


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_search_returns_matching_employee():
    with patch(
        "app.services.employee_service.search_employees",
        return_value=[make_employee()],
    ):
        response = client.get(
            "/employees",
            params={"search": "rahul"},
        )

    assert response.status_code == 200
    assert response.json()[0]["name"] == "Rahul Sharma"


def test_no_matches_returns_empty_list():
    with patch(
        "app.services.employee_service.search_employees",
        return_value=[],
    ):
        response = client.get(
            "/employees",
            params={"search": "zzznomatch"},
        )

    assert response.status_code == 200
    assert response.json() == []


def test_search_over_100_characters_returns_422():
    response = client.get(
        "/employees",
        params={"search": "a" * 101},
    )

    assert response.status_code == 422


def test_validation_error_has_consistent_format():
    response = client.get(
        "/employees",
        params={"search": "a" * 101},
    )

    assert response.status_code == 422

    body = response.json()

    assert body["error"] == "Validation failed"
    assert isinstance(body["details"], list)
    assert body["details"][0]["field"] == "search"
    assert "message" in body["details"][0]


def test_missing_route_returns_404():
    response = client.get("/does-not-exist")

    assert response.status_code == 404
