from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
import os

# Store DB in the backend directory
DB_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assistant.db")
SQLALCHEMY_DATABASE_URL = f"sqlite+aiosqlite:///{DB_FILE}"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, 
    echo=False,
    connect_args={"check_same_thread": False}
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

Base = declarative_base()

async def get_db():
    """Dependency to get the async database session."""
    async with AsyncSessionLocal() as session:
        yield session
