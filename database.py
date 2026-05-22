from sqlalchemy import create_engine, Column, String, Float, Integer, Boolean, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session
from contextlib import contextmanager
import uuid
import os

DB_PATH = os.getenv("DB_PATH", "leads.db")
engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100))
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))
    created_at = Column(DateTime, server_default=func.now())

class Search(Base):
    __tablename__ = "searches"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=True)
    keyword = Column(String(255))
    city = Column(String(100))
    country = Column(String(100))
    category = Column(String(100), nullable=True)
    total_results = Column(Integer, default=0)
    status = Column(String(20), default="pending")
    created_at = Column(DateTime, server_default=func.now())

class Lead(Base):
    __tablename__ = "leads"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    search_id = Column(String, ForeignKey("searches.id"))
    business_name = Column(String(255))
    category = Column(String(100), nullable=True)
    rating = Column(Float, nullable=True)
    reviews_count = Column(Integer, nullable=True)
    address = Column(String(500), nullable=True)
    phone = Column(String(50), nullable=True)
    email = Column(String(255), nullable=True)
    website = Column(String(500), nullable=True)
    maps_url = Column(String(500), nullable=True)
    facebook = Column(String(500), nullable=True)
    instagram = Column(String(500), nullable=True)
    linkedin = Column(String(500), nullable=True)
    has_website = Column(Boolean, default=False)
    website_quality = Column(String(50), nullable=True)
    ai_score = Column(Integer, nullable=True)
    ai_notes = Column(Text, nullable=True)
    suggested_service = Column(String(255), nullable=True)
    outreach_message = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

def init_db():
    Base.metadata.create_all(engine)
    _seed_default_user()

def _seed_default_user():
    import bcrypt
    with get_db() as db:
        exists = db.query(User).filter(User.email == "irfan@leadhunter.com").first()
        if not exists:
            hashed = bcrypt.hashpw("irfan123".encode(), bcrypt.gensalt()).decode()
            db.add(User(
                id=str(uuid.uuid4()),
                name="Muhammad Irfan",
                email="irfan@leadhunter.com",
                password=hashed,
            ))

@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
