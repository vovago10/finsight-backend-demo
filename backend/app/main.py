from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth import router as auth_router
from app.api.budgets import router as budgets_router
from app.api.transactions import router as transactions_router
from app.core.config import settings
from app.core.database import get_db

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="0.1.0",
    description="Sanitized portfolio demo for a personal finance backend.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["System"])
async def health_check():
    return {"status": "ok", "environment": settings.ENVIRONMENT}


@app.get("/health/db", tags=["System"])
async def database_health_check(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(text("SELECT 1"))
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database is unavailable",
        ) from exc

    return {"status": "ok", "database": "reachable"}


app.include_router(auth_router)
app.include_router(budgets_router)
app.include_router(transactions_router)
