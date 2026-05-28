from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from backend.database import AgentStatus, SearchEngine

class AgentCreate(BaseModel):
    name: str
    keywords: str
    search_engine: SearchEngine = SearchEngine.DUCKDUCKGO

class AgentResponse(BaseModel):
    id: int
    name: str
    keywords: str
    search_engine: SearchEngine
    status: AgentStatus
    created_at: datetime
    updated_at: datetime
    progress: int
    total_sites: int
    
    class Config:
        from_attributes = True

class ResultResponse(BaseModel):
    id: int
    agent_id: int
    url: str
    title: Optional[str]
    emails: Optional[str]
    phones: Optional[str]
    addresses: Optional[str]
    company_names: Optional[str]
    social_links: Optional[str]
    contact_forms: Optional[str]
    meta_description: Optional[str]
    scraped_at: datetime
    
    class Config:
        from_attributes = True

class ExportFormat(BaseModel):
    format: str = "json"
