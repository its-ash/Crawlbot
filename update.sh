#!/bin/bash

# Quick update script for production

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}🔄 Updating CrawlBot...${NC}"

# Update backend dependencies
echo -e "${YELLOW}📦 Updating backend...${NC}"
source venv/bin/activate
pip install -r requirements.txt --upgrade
deactivate

# Update and rebuild frontend
echo -e "${YELLOW}🔨 Rebuilding frontend...${NC}"
cd frontend
npm install
npm run build
cd ..

# Reload PM2 processes (zero downtime)
echo -e "${YELLOW}♻️  Reloading services...${NC}"
pm2 reload all

echo -e "${GREEN}✅ Update complete!${NC}"
echo ""
echo "Services status:"
pm2 list
