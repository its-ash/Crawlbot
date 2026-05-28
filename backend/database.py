from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import enum

from backend.config import settings

engine = create_engine(settings.database_url, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class AgentStatus(str, enum.Enum):
    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class SearchEngine(str, enum.Enum):
    GOOGLE = "google"
    DUCKDUCKGO = "duckduckgo"

class Agent(Base):
    __tablename__ = "agents"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    keywords = Column(Text, nullable=False)
    search_engine = Column(SQLEnum(SearchEngine), default=SearchEngine.DUCKDUCKGO)
    status = Column(SQLEnum(AgentStatus), default=AgentStatus.IDLE)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    progress = Column(Integer, default=0)
    total_sites = Column(Integer, default=0)
    
    results = relationship("Result", back_populates="agent", cascade="all, delete-orphan")

class Result(Base):
    __tablename__ = "results"
    
    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(Integer, ForeignKey("agents.id"))
    url = Column(String, nullable=False)
    title = Column(String)
    emails = Column(Text)
    phones = Column(Text)
    addresses = Column(Text)
    company_names = Column(Text)
    social_links = Column(Text)
    contact_forms = Column(Text)
    meta_description = Column(Text)
    scraped_at = Column(DateTime, default=datetime.utcnow)
    
    agent = relationship("Agent", back_populates="results")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    Base.metadata.create_all(bind=engine)
