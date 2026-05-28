import aiohttp
import asyncio
from duckduckgo_search import DDGS
from typing import List, Dict
from backend.config import settings
import time
import random

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
    # Class-level attributes to share rate limiting across all instances
    _last_request_time = 0
    _lock = asyncio.Lock()
    _min_delay = 5.0  # Minimum 5 seconds between requests
    _user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15'
    ]
    
    async def search(self, query: str, num_results: int = 10) -> List[Dict[str, str]]:
        results = []
        max_retries = 3
        base_delay = 15  # Increased from 5 to 15 seconds
        
        for attempt in range(max_retries):
            try:
                # Rate limiting: ensure minimum delay between requests (shared across all instances)
                async with self._lock:
                    current_time = time.time()
                    time_since_last = current_time - self._last_request_time
                    if time_since_last < self._min_delay:
                        wait_time = self._min_delay - time_since_last
                        # Add random jitter to avoid pattern detection
                        wait_time += random.uniform(1, 3)
                        await asyncio.sleep(wait_time)
                    
                    # Run blocking DDGS call in executor to avoid blocking event loop
                    loop = asyncio.get_event_loop()
                    search_results = await loop.run_in_executor(
                        None,
                        self._perform_search,
                        query,
                        num_results
                    )
                    
                    DuckDuckGoSearch._last_request_time = time.time()
                
                for item in search_results:
                    results.append({
                        "title": item.get("title", ""),
                        "url": item.get("href", ""),
                        "snippet": item.get("body", "")
                    })
                
                break  # Success, exit retry loop
                
            except Exception as e:
                error_msg = str(e)
                print(f"DuckDuckGo search error (attempt {attempt + 1}/{max_retries}): {error_msg}")
                
                if "Ratelimit" in error_msg and attempt < max_retries - 1:
                    # Exponential backoff for rate limit errors
                    delay = base_delay * (2 ** attempt)
                    print(f"Rate limited. Waiting {delay} seconds before retry...")
                    await asyncio.sleep(delay)
                elif attempt == max_retries - 1:
                    print(f"Failed after {max_retries} attempts. Returning empty results.")
                else:
                    break  # Non-rate-limit error, don't retry
        
        return results
    
    def _perform_search(self, query: str, num_results: int):
        """Synchronous search operation to run in executor"""
        headers = {
            'User-Agent': random.choice(self._user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
        # Add proxy support if configured
        proxies = None
        if settings.proxy_url:
            proxies = settings.proxy_url
        
        try:
            ddgs = DDGS(headers=headers, timeout=20, proxies=proxies)
            # Use lite=True for less aggressive scraping that's harder to detect
            return list(ddgs.text(query, max_results=num_results, backend="lite"))
        except Exception as e:
            # Fallback to regular backend if lite fails
            if "lite" in str(e).lower() or "backend" in str(e).lower():
                ddgs = DDGS(headers=headers, timeout=20, proxies=proxies)
                return list(ddgs.text(query, max_results=num_results))
            raise

def get_search_engine(engine_type: str) -> SearchEngine:
    if engine_type == "google":
        return GoogleSearch()
    else:
        return DuckDuckGoSearch()
