#!/bin/bash

# Deployment verification script

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

DOMAIN="crawler.ash-api.online"
API_URL="https://${DOMAIN}/api"
WS_URL="wss://${DOMAIN}/ws"

echo -e "${BLUE}🔍 CrawlBot Deployment Verification${NC}"
echo ""

# Check DNS
echo -e "${YELLOW}Checking DNS...${NC}"
if host ${DOMAIN} > /dev/null 2>&1; then
    echo -e "${GREEN}✅ DNS configured${NC}"
    host ${DOMAIN}
else
    echo -e "${RED}❌ DNS not configured${NC}"
fi
echo ""

# Check Nginx
echo -e "${YELLOW}Checking Nginx...${NC}"
if systemctl is-active --quiet nginx; then
    echo -e "${GREEN}✅ Nginx is running${NC}"
else
    echo -e "${RED}❌ Nginx is not running${NC}"
fi
echo ""

# Check SSL certificate
echo -e "${YELLOW}Checking SSL certificate...${NC}"
if [ -d "/etc/letsencrypt/live/${DOMAIN}" ]; then
    echo -e "${GREEN}✅ SSL certificate exists${NC}"
    sudo certbot certificates | grep ${DOMAIN}
else
    echo -e "${RED}❌ SSL certificate not found${NC}"
fi
echo ""

# Check PM2 processes
echo -e "${YELLOW}Checking PM2 processes...${NC}"
if pm2 list | grep -q "crawlbot-backend"; then
    echo -e "${GREEN}✅ Backend process running${NC}"
else
    echo -e "${RED}❌ Backend process not running${NC}"
fi

if pm2 list | grep -q "crawlbot-frontend"; then
    echo -e "${GREEN}✅ Frontend process running${NC}"
else
    echo -e "${RED}❌ Frontend process not running${NC}"
fi
echo ""

# Check frontend build
echo -e "${YELLOW}Checking frontend build...${NC}"
if [ -d "/home/Crawlbot/frontend/dist" ]; then
    echo -e "${GREEN}✅ Frontend build exists${NC}"
else
    echo -e "${RED}❌ Frontend build not found${NC}"
    echo "   Run: cd frontend && npm run build"
fi
echo ""

# Check .env file
echo -e "${YELLOW}Checking environment configuration...${NC}"
if [ -f "/home/Crawlbot/.env" ]; then
    echo -e "${GREEN}✅ .env file exists${NC}"
    if grep -q "LOGIN_TOKEN=crawlbot2026" /home/Crawlbot/.env; then
        echo -e "${YELLOW}⚠️  WARNING: Using default LOGIN_TOKEN${NC}"
        echo "   Update LOGIN_TOKEN in .env for security"
    fi
else
    echo -e "${RED}❌ .env file not found${NC}"
fi
echo ""

# Check ports
echo -e "${YELLOW}Checking ports...${NC}"
if netstat -tlnp 2>/dev/null | grep -q ":8000"; then
    echo -e "${GREEN}✅ Backend port 8000 listening${NC}"
else
    echo -e "${RED}❌ Backend port 8000 not listening${NC}"
fi

if netstat -tlnp 2>/dev/null | grep -q ":80"; then
    echo -e "${GREEN}✅ HTTP port 80 listening${NC}"
else
    echo -e "${RED}❌ HTTP port 80 not listening${NC}"
fi

if netstat -tlnp 2>/dev/null | grep -q ":443"; then
    echo -e "${GREEN}✅ HTTPS port 443 listening${NC}"
else
    echo -e "${RED}❌ HTTPS port 443 not listening${NC}"
fi
echo ""

# Check firewall
echo -e "${YELLOW}Checking firewall...${NC}"
if command -v ufw &> /dev/null; then
    if sudo ufw status | grep -q "Status: active"; then
        echo -e "${GREEN}✅ Firewall active${NC}"
        sudo ufw status | grep -E "(80|443|22)"
    else
        echo -e "${YELLOW}⚠️  Firewall not active${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  UFW not installed${NC}"
fi
echo ""

# Test HTTP/HTTPS
echo -e "${YELLOW}Testing website access...${NC}"
if curl -s -o /dev/null -w "%{http_code}" https://${DOMAIN} | grep -q "200"; then
    echo -e "${GREEN}✅ Website accessible via HTTPS${NC}"
else
    echo -e "${RED}❌ Website not accessible${NC}"
fi
echo ""

# Summary
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}📋 Summary${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "Application URL: https://${DOMAIN}"
echo "API Docs:       https://${DOMAIN}/docs"
echo ""
echo "PM2 Status:"
pm2 list
echo ""
echo -e "${YELLOW}For detailed logs, run:${NC}"
echo "  pm2 logs"
echo "  sudo tail -f /var/log/nginx/crawlbot-error.log"
echo ""
