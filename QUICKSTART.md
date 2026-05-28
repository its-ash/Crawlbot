# Quick Start Guide

## Prerequisites Checklist

- [ ] Python 3.9+ installed
- [ ] Node.js 18+ installed
- [ ] Ollama installed (optional but recommended for LLM features)

## 1. Install Ollama (Recommended)

```bash
# macOS/Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Then pull the model
ollama pull llama3
```

## 2. Configure Environment (Optional)

If you want to use Google Search API:

1. Get Google Custom Search API key: https://developers.google.com/custom-search/v1/overview
2. Create Custom Search Engine: https://programmablesearchengine.google.com/
3. Edit `.env` file and add:
   ```
   GOOGLE_API_KEY=your_key_here
   GOOGLE_CSE_ID=your_cse_id_here
   ```

**Note**: DuckDuckGo works out of the box with no API key required!

## 3. Quick Start

### Option A: Using Start Script (Easiest)

**macOS/Linux:**
```bash
./start.sh
```

**Windows:**
```cmd
start.bat
```

### Option B: Manual Start

**Terminal 1 - Backend:**
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
playwright install chromium

# Start server
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## 4. Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 5. Create Your First Agent

1. Click "Create New Agent"
2. Enter:
   - **Name**: "Test Agent"
   - **Keywords**: "coffee shops San Francisco contact"
   - **Search Engine**: DuckDuckGo (or Google if configured)
3. Click "Start" on the agent card
4. Watch the real-time progress
5. Click "View" to see extracted data
6. Export results as JSON or CSV

## Troubleshooting

### Backend won't start
```bash
# Make sure port 8000 is free
lsof -ti:8000 | xargs kill -9

# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

### Frontend won't start
```bash
# Clear node_modules and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Playwright browser issues
```bash
# Reinstall browsers
playwright install --force chromium
```

### Ollama not connecting
```bash
# Start Ollama service
ollama serve

# Verify it's running
curl http://localhost:11434/api/version
```

## Performance Tips

- Start with 5-10 search results per agent
- Run 3-5 agents concurrently for optimal performance
- Use DuckDuckGo for unlimited searches
- Use Google for higher quality results (limited to 100/day on free tier)

## Next Steps

- Read [README.md](README.md) for complete documentation
- Check [DESIGN.md](DESIGN.md) for UI customization
- Explore API at http://localhost:8000/docs

Happy crawling! 🤖
