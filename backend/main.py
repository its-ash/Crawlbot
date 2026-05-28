from fastapi import FastAPI, Depends, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import asyncio
import csv
import io
import json

from backend.database import get_db, init_db, Agent, Result, AgentStatus
from backend.schemas import AgentCreate, AgentResponse, ResultResponse
from backend.worker import WorkerPool
from backend.websocket import WebSocketManager

app = FastAPI(title="CrawlBot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

websocket_manager = WebSocketManager()
worker_pool = WorkerPool(websocket_manager)

@app.on_event("startup")
async def startup_event():
    init_db()

@app.get("/")
async def root():
    return {"message": "CrawlBot API is running"}

@app.post("/api/agents", response_model=AgentResponse)
async def create_agent(agent_data: AgentCreate, db: Session = Depends(get_db)):
    agent = Agent(
        name=agent_data.name,
        keywords=agent_data.keywords,
        search_engine=agent_data.search_engine,
        status=AgentStatus.IDLE
    )
    db.add(agent)
    db.commit()
    db.refresh(agent)
    return agent

@app.get("/api/agents", response_model=List[AgentResponse])
async def get_agents(db: Session = Depends(get_db)):
    agents = db.query(Agent).order_by(Agent.created_at.desc()).all()
    return agents

@app.get("/api/agents/{agent_id}", response_model=AgentResponse)
async def get_agent(agent_id: int, db: Session = Depends(get_db)):
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent

@app.delete("/api/agents/{agent_id}")
async def delete_agent(agent_id: int, db: Session = Depends(get_db)):
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    if worker_pool.is_agent_running(agent_id):
        worker_pool.stop_agent(agent_id)
    
    db.delete(agent)
    db.commit()
    return {"message": "Agent deleted"}

@app.post("/api/agents/{agent_id}/start")
async def start_agent(agent_id: int, db: Session = Depends(get_db)):
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    if worker_pool.is_agent_running(agent_id):
        raise HTTPException(status_code=400, detail="Agent already running")
    
    asyncio.create_task(worker_pool.start_agent(agent_id, db))
    
    return {"message": "Agent started"}

@app.post("/api/agents/{agent_id}/stop")
async def stop_agent(agent_id: int, db: Session = Depends(get_db)):
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    worker_pool.stop_agent(agent_id)
    
    agent.status = AgentStatus.IDLE
    db.commit()
    
    return {"message": "Agent stopped"}

@app.get("/api/agents/{agent_id}/results", response_model=List[ResultResponse])
async def get_agent_results(agent_id: int, db: Session = Depends(get_db)):
    results = db.query(Result).filter(Result.agent_id == agent_id).all()
    return results

@app.get("/api/agents/{agent_id}/export/json")
async def export_results_json(agent_id: int, db: Session = Depends(get_db)):
    results = db.query(Result).filter(Result.agent_id == agent_id).all()
    
    data = []
    for result in results:
        data.append({
            "url": result.url,
            "title": result.title,
            "emails": result.emails.split(",") if result.emails else [],
            "phones": result.phones.split(",") if result.phones else [],
            "addresses": result.addresses.split(",") if result.addresses else [],
            "company_names": result.company_names.split(",") if result.company_names else [],
            "social_links": result.social_links,
            "contact_forms": result.contact_forms.split(",") if result.contact_forms else [],
            "meta_description": result.meta_description,
            "scraped_at": result.scraped_at.isoformat()
        })
    
    return data

@app.get("/api/agents/{agent_id}/export/csv")
async def export_results_csv(agent_id: int, db: Session = Depends(get_db)):
    results = db.query(Result).filter(Result.agent_id == agent_id).all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    writer.writerow([
        "URL", "Title", "Emails", "Phones", "Addresses", 
        "Company Names", "Social Links", "Contact Forms", 
        "Meta Description", "Scraped At"
    ])
    
    for result in results:
        writer.writerow([
            result.url,
            result.title,
            result.emails,
            result.phones,
            result.addresses,
            result.company_names,
            result.social_links,
            result.contact_forms,
            result.meta_description,
            result.scraped_at.isoformat()
        ])
    
    return {"csv": output.getvalue()}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket_manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)
