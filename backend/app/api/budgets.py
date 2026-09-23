from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.core.database import get_db
from app.models import Budget, Transaction, User
from app.schemas import BudgetCreate, BudgetResponse, SummaryResponse

router = APIRouter(tags=["Budgets"])


@router.post("/budgets", response_model=BudgetResponse, status_code=201)
async def upsert_budget(
    payload: BudgetCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Budget:
    result = await db.execute(
        select(Budget).where(
            Budget.user_id == current_user.id,
            Budget.category == payload.category,
            Budget.period == payload.period,
        )
    )
    budget = result.scalar_one_or_none()

    if budget:
        budget.limit_amount = payload.limit_amount
    else:
        budget = Budget(
            user_id=current_user.id,
            category=payload.category,
            period=payload.period,
            limit_amount=payload.limit_amount,
        )
        db.add(budget)

    await db.commit()
    await db.refresh(budget)
    return budget


@router.get("/budgets", response_model=list[BudgetResponse])
async def list_budgets(
    month: str = Query(pattern=r"^\d{4}-\d{2}$"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[Budget]:
    result = await db.execute(
        select(Budget)
        .where(Budget.user_id == current_user.id, Budget.period == month)
        .order_by(Budget.category)
    )
    return list(result.scalars().all())


@router.get("/summary", response_model=SummaryResponse)
async def read_monthly_summary(
    month: str = Query(pattern=r"^\d{4}-\d{2}$"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> SummaryResponse:
    result = await db.execute(
        select(Transaction).where(
            Transaction.user_id == current_user.id,
            Transaction.transaction_date >= date.fromisoformat(f"{month}-01"),
            Transaction.transaction_date < _next_month_start(month),
        )
    )
    transactions = result.scalars().all()

    income = sum(tx.amount for tx in transactions if tx.amount > 0)
    expenses = abs(sum(tx.amount for tx in transactions if tx.amount < 0))
    by_category: dict[str, int] = {}

    for tx in transactions:
        if tx.amount < 0:
            by_category[tx.category] = by_category.get(tx.category, 0) + abs(tx.amount)

    return SummaryResponse(
        month=month,
        income=income,
        expenses=expenses,
        balance=income - expenses,
        by_category=by_category,
    )


def _next_month_start(month: str) -> date:
    year, month_number = [int(part) for part in month.split("-")]
    if month_number == 12:
        return date(year + 1, 1, 1)
    return date(year, month_number + 1, 1)
