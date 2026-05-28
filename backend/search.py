import aiohttp
from duckduckgo_search import DDGS
from typing import List, Dict
from backend.config import settings

class SearchEngine:
    async def search(self, query: str, num_results: int = 10) -> List[Dict[str, str]]:
        raise NotImplementedError

class GoogleSearch(SearchEngine):
    async def search(self, query: str, num_results: int = 10) -> List[Dict[str, str]]:
        if not settings.google_api_key or not settings.google_cse_id:
            raise ValueError("Google API credentials not configured")
        
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": settings.google_api_key,
            "cx": settings.google_cse_id,
            "q": query,
            "num": min(num_results, 10)
        }
        
        results = []
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    for item in data.get("items", []):
                        results.append({
                            "title": item.get("title", ""),
                            "url": item.get("link", ""),
                            "snippet": item.get("snippet", "")
                        })
        
        return results

class DuckDuckGoSearch(SearchEngine):
    async def search(self, query: str, num_results: int = 10) -> List[Dict[str, str]]:
        results = []
        try:
            ddgs = DDGS()
            search_results = ddgs.text(query, max_results=num_results)
            
            for item in search_results:
                results.append({
                    "title": item.get("title", ""),
                    "url": item.get("href", ""),
                    "snippet": item.get("body", "")
                })
        except Exception as e:
            print(f"DuckDuckGo search error: {e}")
        
        return results

def get_search_engine(engine_type: str) -> SearchEngine:
    if engine_type == "google":
        return GoogleSearch()
    else:
        return DuckDuckGoSearch()
