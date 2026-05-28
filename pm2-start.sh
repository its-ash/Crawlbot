#!/bin/bash

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}🤖 CrawlBot PM2 Manager${NC}"
echo ""

# Create logs directory if it doesn't exist
mkdir -p logs

# Check if PM2 is installed
if ! command -v pm2 &> /dev/null; then
    echo -e "${RED}❌ PM2 is not installed${NC}"
    echo "Install PM2 with: npm install -g pm2"
    exit 1
fi

# Check if virtual environment exists
if [ ! -f "venv/bin/uvicorn" ]; then
    echo -e "${YELLOW}⚠️  Virtual environment not found. Creating...${NC}"
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    playwright install chromium
fi

# Check if frontend dependencies are installed
if [ ! -d "frontend/node_modules" ]; then
    echo -e "${YELLOW}⚠️  Frontend dependencies not found. Installing...${NC}"
    cd frontend
    npm install
    cd ..
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  .env file not found. Creating from .env.example...${NC}"
    cp .env.example .env
    echo -e "${YELLOW}⚠️  Please edit .env file and set your LOGIN_TOKEN${NC}"
fi

# Start PM2 processes
echo -e "${GREEN}🚀 Starting CrawlBot with PM2...${NC}"
pm2 start ecosystem.config.js

echo ""
echo -e "${GREEN}✅ Services started!${NC}"
echo ""
echo "Available commands:"
echo "  pm2 list          - View all processes"
echo "  pm2 logs          - View logs"
echo "  pm2 monit         - Monitor in real-time"
echo "  pm2 restart all   - Restart all services"
echo "  pm2 stop all      - Stop all services"
echo ""
echo "Access the application:"
echo "  Frontend: http://localhost:5173"
echo "  Backend:  http://localhost:8000"
echo "  API Docs: http://localhost:8000/docs"
echo ""
