#!/bin/bash

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}🛑 Stopping CrawlBot PM2 Services...${NC}"

pm2 stop ecosystem.config.js
pm2 delete ecosystem.config.js

echo ""
echo -e "${GREEN}✅ All services stopped and removed${NC}"
echo ""
