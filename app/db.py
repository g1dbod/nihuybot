import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from dotenv import load_dotenv

load_dotenv()

# Параметры подключения берутся из переменных окружения (они же пойдут в Docker)
POSTGRES_USER = os.getenv("POSTGRES_USER", "bot_user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "supersecret")
POSTGRES_DB = os.getenv("POSTGRES_DB", "bot_db")
# В docker-compose хост будет называться 'db'
DB_HOST = os.getenv("DB_HOST", "db") 

DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:5432/{POSTGRES_DB}"

engine = create_async_engine(DATABASE_URL, echo=False)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(unique=True, index=True)
    username: Mapped[str | None]
    first_name: Mapped[str]
    last_name: Mapped[str | None]
    is_active: Mapped[bool] = mapped_column(default=True)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session