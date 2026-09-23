from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: str
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class BudgetCreate(BaseModel):
    category: str = Field(min_length=2, max_length=80)
    period: str = Field(pattern=r"^\d{4}-\d{2}$")
    limit_amount: int = Field(ge=0)


class BudgetResponse(BaseModel):
    id: str
    category: str
    period: str
    limit_amount: int

    model_config = ConfigDict(from_attributes=True)


class TransactionCreate(BaseModel):
    category: str = Field(min_length=2, max_length=80)
    description: str = Field(min_length=1, max_length=255)
    amount: int
    transaction_date: date


class TransactionResponse(BaseModel):
    id: str
    category: str
    description: str
    amount: int
    transaction_date: date

    model_config = ConfigDict(from_attributes=True)


class SummaryResponse(BaseModel):
    month: str
    income: int
    expenses: int
    balance: int
    by_category: dict[str, int]
