from datetime import date

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.core.database import get_db
from app.models import Transaction, User
from app.schemas import TransactionCreate, TransactionResponse

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.post("", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    payload: TransactionCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Transaction:
    transaction = Transaction(
        user_id=current_user.id,
        category=payload.category,
        description=payload.description,
        amount=payload.amount,
        transaction_date=payload.transaction_date,
    )
    db.add(transaction)
    await db.commit()
    await db.refresh(transaction)
    return transaction


@router.get("", response_model=list[TransactionResponse])
async def list_transactions(
    from_date: date | None = Query(default=None, alias="from"),
    to_date: date | None = Query(default=None, alias="to"),
    category: str | None = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[Transaction]:
    query = select(Transaction).where(Transaction.user_id == current_user.id)

    if from_date:
        query = query.where(Transaction.transaction_date >= from_date)
    if to_date:
        query = query.where(Transaction.transaction_date <= to_date)
    if category:
        query = query.where(Transaction.category == category)

    query = query.order_by(Transaction.transaction_date.desc())
    result = await db.execute(query)
    return list(result.scalars().all())


@router.post(
    "/seed-demo",
    response_model=list[TransactionResponse],
    status_code=status.HTTP_201_CREATED,
)
async def seed_demo_transactions(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[Transaction]:
    examples = [
        Transaction(
            user_id=current_user.id,
            category="salary",
            description="Demo salary",
            amount=80_000,
            transaction_date=date(2026, 9, 1),
        ),
        Transaction(
            user_id=current_user.id,
            category="groceries",
            description="Demo grocery store",
            amount=-4_500,
            transaction_date=date(2026, 9, 5),
        ),
        Transaction(
            user_id=current_user.id,
            category="transport",
            description="Demo public transport",
            amount=-900,
            transaction_date=date(2026, 9, 7),
        ),
        Transaction(
            user_id=current_user.id,
            category="subscriptions",
            description="Demo streaming subscription",
            amount=-350,
            transaction_date=date(2026, 9, 10),
        ),
    ]

    db.add_all(examples)
    await db.commit()

    for transaction in examples:
        await db.refresh(transaction)

    return examples
