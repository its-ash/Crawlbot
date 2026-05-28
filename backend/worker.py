import asyncio
from typing import Dict, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from backend.database import Agent, Result, AgentStatus
from backend.search import get_search_engine
from backend.scraper import WebScraper
from backend.llm import LLMExtractor
from backend.config import settings

class AgentWorker:
    def __init__(self, agent_id: int, db: Session, websocket_manager):
        self.agent_id = agent_id
        self.db = db
        self.websocket_manager = websocket_manager
        self.is_running = False
    
    async def run(self):
        self.is_running = True
        
        agent = self.db.query(Agent).filter(Agent.id == self.agent_id).first()
        if not agent:
            return
        
        agent.status = AgentStatus.RUNNING
        agent.updated_at = datetime.utcnow()
        self.db.commit()
        
        await self.websocket_manager.broadcast({
            "type": "agent_update",
            "agent_id": self.agent_id,
            "status": "running"
        })
        
        try:
            search_engine = get_search_engine(agent.search_engine.value)
            search_results = await search_engine.search(
                agent.keywords,
                num_results=settings.results_per_search
            )
            
            agent.total_sites = len(search_results)
            self.db.commit()
            
            async with WebScraper() as scraper:
                llm_extractor = LLMExtractor()
                
                for idx, search_result in enumerate(search_results):
                    if not self.is_running:
                        break
                    
                    url = search_result["url"]
                    
                    scraped_data = await scraper.scrape_page(url)
                    
                    if "error" not in scraped_data:
                        enhanced_data = await llm_extractor.enhance_extraction(scraped_data)
                        
                        result = Result(
                            agent_id=self.agent_id,
                            url=enhanced_data.get("url"),
                            title=enhanced_data.get("title"),
                            emails=",".join(enhanced_data.get("emails", [])),
                            phones=",".join(enhanced_data.get("phones", [])),
                            addresses=",".join(enhanced_data.get("addresses", [])),
                            company_names=",".join(enhanced_data.get("company_names", [])),
                            social_links=str(enhanced_data.get("social_links", {})),
                            contact_forms=",".join(enhanced_data.get("contact_forms", [])),
                            meta_description=enhanced_data.get("meta_description")
                        )
                        
                        self.db.add(result)
                    
                    agent.progress = idx + 1
                    self.db.commit()
                    
                    # Get current results count
                    results_count = self.db.query(Result).filter(Result.agent_id == self.agent_id).count()
                    
                    await self.websocket_manager.broadcast({
                        "type": "progress_update",
                        "agent_id": self.agent_id,
                        "progress": agent.progress,
                        "total": agent.total_sites,
                        "results_count": results_count
                    })
            
            agent.status = AgentStatus.COMPLETED
            agent.updated_at = datetime.utcnow()
            self.db.commit()
            
            await self.websocket_manager.broadcast({
                "type": "agent_update",
                "agent_id": self.agent_id,
                "status": "completed"
            })
        
        except Exception as e:
            print(f"Agent {self.agent_id} error: {e}")
            agent.status = AgentStatus.FAILED
            agent.updated_at = datetime.utcnow()
            self.db.commit()
            
            await self.websocket_manager.broadcast({
                "type": "agent_update",
                "agent_id": self.agent_id,
                "status": "failed"
            })
        
        finally:
            self.is_running = False

class WorkerPool:
    def __init__(self, websocket_manager):
        self.workers: Dict[int, asyncio.Task] = {}
        self.semaphore = asyncio.Semaphore(settings.max_concurrent_agents)
        self.websocket_manager = websocket_manager
    
    async def start_agent(self, agent_id: int, db: Session):
        async with self.semaphore:
            worker = AgentWorker(agent_id, db, self.websocket_manager)
            task = asyncio.create_task(worker.run())
            self.workers[agent_id] = task
            
            try:
                await task
            finally:
                if agent_id in self.workers:
                    del self.workers[agent_id]
    
    def stop_agent(self, agent_id: int):
        if agent_id in self.workers:
            self.workers[agent_id].cancel()
            del self.workers[agent_id]
    
    def is_agent_running(self, agent_id: int) -> bool:
        return agent_id in self.workers
