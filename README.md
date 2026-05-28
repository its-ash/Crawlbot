# CrawlBot - Marketing Data Extraction Agent

A powerful web scraping agent system that searches the internet, visits websites, and extracts marketing-relevant data including emails, phone numbers, addresses, company information, and social media links. Features an industrial skeuomorphic UI and real-time progress tracking.

## Features

- 🤖 **Multiple Concurrent Agents**: Run up to 10 agents simultaneously
- 🔍 **Dual Search Engines**: Google Custom Search API & DuckDuckGo
- 🌐 **Intelligent Scraping**: Playwright-based browser automation handles JavaScript-heavy sites
- 🧠 **LLM Enhancement**: Ollama/Llama model for intelligent data extraction
- 📊 **Real-time Updates**: WebSocket-powered live progress tracking
- 📤 **Export Options**: Download results as JSON or CSV
- 🎨 **Industrial UI**: Unique skeuomorphic design with tactile interactions

## Extracted Data Fields

- Email addresses
- Phone numbers
- Physical addresses
- Company/Business names
- Social media links (Facebook, Twitter/X, LinkedIn, Instagram, YouTube, TikTok)
- Contact form URLs
- Website meta descriptions

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - Database ORM
- **Playwright** - Browser automation
- **Ollama** - Local LLM integration
- **WebSockets** - Real-time updates

### Frontend
- **Vue 3** - Progressive JavaScript framework
- **Tailwind CSS** - Utility-first styling
- **Lucide Icons** - Beautiful icon set
- **Axios** - HTTP client

## Installation

### Prerequisites

1. **Python 3.9+**
2. **Node.js 18+**
3. **Ollama** (for LLM features)

### Backend Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium

# Copy environment file
cp .env.example .env

# Edit .env and add your API keys (optional for Google)
# GOOGLE_API_KEY=your_key_here
# GOOGLE_CSE_ID=your_cse_id_here
```

### Frontend Setup

```bash
cd frontend
npm install
```

### Ollama Setup (Optional but Recommended)

```bash
# Install Ollama from https://ollama.ai
# Pull Llama model
ollama pull llama3
```

## Running the Application

### Start Backend

```bash
# From project root
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### Start Frontend

```bash
# In another terminal
cd frontend
npm run dev
```

Visit `http://localhost:5173` in your browser.

## Usage

1. **Create an Agent**
   - Click "Create New Agent"
   - Enter agent name (e.g., "Real Estate Leads California")
   - Enter search keywords (e.g., "real estate agents Los Angeles contact")
   - Choose search engine (DuckDuckGo or Google)

2. **Start the Agent**
   - Click "Start" on the agent card
   - Watch real-time progress updates
   - LED indicator shows status (yellow=running, green=completed)

3. **View Results**
   - Click "View" to see extracted data
   - Export to JSON or CSV format

## Configuration

Edit `.env` file:

```env
# Google Search (optional - requires API key)
GOOGLE_API_KEY=your_google_api_key
GOOGLE_CSE_ID=your_custom_search_engine_id

# Ollama LLM
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3

# Database
DATABASE_URL=sqlite:///./crawlbot.db

# Worker Settings
MAX_CONCURRENT_AGENTS=10
RESULTS_PER_SEARCH=10
```

## API Endpoints

- `POST /api/agents` - Create new agent
- `GET /api/agents` - List all agents
- `GET /api/agents/{id}` - Get agent details
- `POST /api/agents/{id}/start` - Start agent
- `POST /api/agents/{id}/stop` - Stop agent
- `DELETE /api/agents/{id}` - Delete agent
- `GET /api/agents/{id}/results` - Get results
- `GET /api/agents/{id}/export/json` - Export JSON
- `GET /api/agents/{id}/export/csv` - Export CSV
- `WS /ws` - WebSocket for real-time updates

## Project Structure

```
Crawlbot/
├── backend/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration
│   ├── database.py          # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── search.py            # Search engines
│   ├── scraper.py           # Web scraper
│   ├── llm.py               # LLM integration
│   ├── worker.py            # Agent worker pool
│   └── websocket.py         # WebSocket manager
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── AgentCard.vue
│   │   │   ├── CreateAgentModal.vue
│   │   │   └── ResultsModal.vue
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── App.vue
│   │   ├── main.js
│   │   └── style.css
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── requirements.txt
├── .env.example
├── .gitignore
├── DESIGN.md
└── README.md
```

## Design System

The UI follows an **Industrial Skeuomorphism** design philosophy featuring:

- Neumorphic shadows (dual highlight/shadow)
- Physical button press animations
- LED status indicators with glow effects
- Monospace typography for technical data
- Tactile 3D card interactions
- Safety orange accent color

See [DESIGN.md](DESIGN.md) for complete design documentation.

## Troubleshooting

**Playwright fails to launch browser:**
```bash
playwright install chromium
```

**Ollama connection error:**
- Ensure Ollama is running: `ollama serve`
- Check `OLLAMA_BASE_URL` in `.env`

**Google Search not working:**
- Verify API key and CSE ID in `.env`
- Use DuckDuckGo as alternative (no API key needed)

**WebSocket connection fails:**
- Check CORS settings in backend
- Verify WebSocket URL in frontend

## License

MIT

## Contributing

Pull requests welcome! Please maintain the industrial design aesthetic when adding UI features.

---

Built with ❤️ using FastAPI, Vue 3, and Playwright
