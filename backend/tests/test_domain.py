import unittest
from datetime import date

from app.api.budgets import _next_month_start
from app.core.security import create_access_token, hash_password, verify_password
from app.models import Budget


class DomainTests(unittest.TestCase):
    def test_password_hashing_does_not_store_plain_text(self) -> None:
        hashed = hash_password("password123")

        self.assertNotEqual(hashed, "password123")
        self.assertTrue(verify_password("password123", hashed))
        self.assertFalse(verify_password("wrong-password", hashed))

    def test_access_token_is_created(self) -> None:
        token = create_access_token(user_id="user-id", email="demo@example.com")

        self.assertGreater(len(token), 20)

    def test_budget_model_has_unique_user_category_period_constraint(self) -> None:
        constraint_names = {constraint.name for constraint in Budget.__table__.constraints}

        self.assertIn("uq_budgets_user_category_period", constraint_names)

    def test_next_month_start_handles_regular_month_and_year_boundary(self) -> None:
        self.assertEqual(_next_month_start("2026-09"), date(2026, 10, 1))
        self.assertEqual(_next_month_start("2026-12"), date(2027, 1, 1))
