import unittest

from fastapi.testclient import TestClient

from app.core.database import get_db
from app.main import app


class HealthySession:
    async def execute(self, statement):
        return None


class BrokenSession:
    async def execute(self, statement):
        raise RuntimeError("database unavailable")


class HealthEndpointTests(unittest.TestCase):
    def tearDown(self) -> None:
        app.dependency_overrides.clear()

    def test_health_endpoint_returns_ok(self) -> None:
        with TestClient(app) as client:
            response = client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")

    def test_database_health_endpoint_returns_ok(self) -> None:
        async def override_get_db():
            yield HealthySession()

        app.dependency_overrides[get_db] = override_get_db

        with TestClient(app) as client:
            response = client.get("/health/db")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok", "database": "reachable"})

    def test_database_health_endpoint_returns_503(self) -> None:
        async def override_get_db():
            yield BrokenSession()

        app.dependency_overrides[get_db] = override_get_db

        with TestClient(app) as client:
            response = client.get("/health/db")

        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json()["detail"], "Database is unavailable")
