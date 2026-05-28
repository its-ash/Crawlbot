# DuckDuckGo Rate Limit Solutions

## Problem
DuckDuckGo aggressively rate limits automated searches to prevent scraping abuse. You'll see errors like:
```
DuckDuckGoSearchException: Ratelimit
```

## Implemented Solutions

### 1. **Rate Limiting & Delays** ✅
- Minimum 5 seconds between requests
- Random jitter (1-3 seconds) to avoid pattern detection
- Exponential backoff: 15s → 30s → 60s on rate limit errors
- Shared state across all agents to prevent concurrent requests

### 2. **Request Disguising** ✅
- Rotating user agents (5 different browsers)
- Realistic HTTP headers
- "lite" backend for less aggressive scraping
- 20-second timeout for stability

### 3. **Proxy Support** ✅
Add to your `.env` file:
```bash
PROXY_URL=http://user:pass@proxy.example.com:8080
# or
PROXY_URL=socks5://proxy.example.com:1080
```

## Recommended Solutions

### Option A: Use Google Custom Search (Best)
Google provides 100 free searches/day with no rate limit issues:

1. Get API key: https://console.cloud.google.com/apis/credentials
2. Create CSE: https://programmablesearchengine.google.com/
3. Add to `.env`:
```bash
GOOGLE_API_KEY=your_api_key_here
GOOGLE_CSE_ID=your_cse_id_here
```
4. Select "Google" as search engine when creating agents

### Option B: Use a Proxy Service
Free/paid proxy services to avoid IP bans:
- **Free**: Tor, ProxyMesh free tier
- **Paid**: Bright Data, Oxylabs, SmartProxy (residential IPs)
- **Rotating Proxies**: Change IP per request

### Option C: Reduce Search Frequency
In [backend/config.py](backend/config.py), set:
```python
results_per_search: int = 5  # Reduced from 10
max_concurrent_agents: int = 1  # Only one agent at a time
```

### Option D: Use Alternative Search APIs
Replace DuckDuckGo with:
- **SerpAPI** (https://serpapi.com/) - $50/month for 5000 searches
- **Brave Search API** (https://brave.com/search/api/) - Free tier available
- **Bing Search API** (https://www.microsoft.com/en-us/bing/apis/bing-web-search-api)

## Current Implementation Details

**File**: [backend/search.py](backend/search.py)

- Class-level rate limiting (shared across all instances)
- AsyncIO locks for thread-safe operation
- Executor pattern for non-blocking searches
- Automatic fallback between backends
- Comprehensive error handling with retries

## Testing the Fix

Restart your application:
```bash
./start.sh
```

Monitor the logs - you should see:
```
Rate limited. Waiting 15 seconds before retry...
Rate limited. Waiting 30 seconds before retry...
```

If still failing after 3 attempts, consider using Google Custom Search or a proxy.
