
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import NullPool

DATABASE_URL = "postgresql+asyncpg://postgres:password@localhost:5432/chatroom"


engine = create_async_engine(
    DATABASE_URL, 
    echo=True,
    poolclass=NullPool  # No connection pooling - create fresh connection each time
)
AsyncSessionLocal = async_sessionmaker(
	bind=engine,
	class_=AsyncSession,
	expire_on_commit=False
)
Base = declarative_base()