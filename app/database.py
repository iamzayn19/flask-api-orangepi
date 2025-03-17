from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import DATABASE_URL  # Ensure DATABASE_URL is correctly set

# ✅ Initialize Database Connection
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ Define Base (DON'T import models here)
Base = declarative_base()

def get_db():
    """
    Dependency Injection for getting database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
