import unittest
from datetime import date

from pydantic import ValidationError

from app.schemas import BudgetCreate, TransactionCreate, UserCreate


class SchemaTests(unittest.TestCase):
    def test_user_create_requires_valid_email_and_password_length(self) -> None:
        payload = UserCreate(email="demo@example.com", password="password123")

        self.assertEqual(payload.email, "demo@example.com")

        with self.assertRaises(ValidationError):
            UserCreate(email="invalid-email", password="password123")

        with self.assertRaises(ValidationError):
            UserCreate(email="demo@example.com", password="short")

    def test_budget_create_requires_yyyy_mm_period(self) -> None:
        payload = BudgetCreate(category="groceries", period="2026-09", limit_amount=10_000)

        self.assertEqual(payload.period, "2026-09")

        with self.assertRaises(ValidationError):
            BudgetCreate(category="groceries", period="09-2026", limit_amount=10_000)

    def test_transaction_create_accepts_minor_unit_amounts(self) -> None:
        payload = TransactionCreate(
            category="groceries",
            description="Demo grocery store",
            amount=-4_500,
            transaction_date=date(2026, 9, 5),
        )

        self.assertEqual(payload.amount, -4_500)
        self.assertEqual(payload.transaction_date, date(2026, 9, 5))
