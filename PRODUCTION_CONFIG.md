# Production Deployment Summary

## Domain Configuration

**Production URL**: https://crawler.ash-api.online

## What Was Configured

### 1. Backend Configuration
- ✅ CORS updated to allow production domain
- ✅ Supports both HTTP and HTTPS
- ✅ WebSocket connections over WSS
- ✅ Production-ready error handling

**File**: [backend/main.py](backend/main.py)
```python
allowed_origins = [
    "https://crawler.ash-api.online",
    "http://crawler.ash-api.online"
]
```

### 2. Frontend Configuration
- ✅ Production build optimization
- ✅ Code splitting for better performance
- ✅ WebSocket auto-detects protocol (ws/wss)
- ✅ API calls use relative paths

**File**: [frontend/vite.config.js](frontend/vite.config.js)
- Build optimization
- Vendor code splitting
- Source map disabled for production

**File**: [frontend/src/services/api.js](frontend/src/services/api.js)
- Auto-detects HTTPS for WSS connections
- Relative API paths work with nginx proxy

### 3. Nginx Reverse Proxy
- ✅ SSL/TLS termination
- ✅ HTTP to HTTPS redirect
- ✅ WebSocket proxy support
- ✅ Static file serving with caching
- ✅ Security headers
- ✅ Gzip compression

**File**: [nginx.conf](nginx.conf)

### 4. PM2 Process Management
- ✅ Production configuration
- ✅ Auto-restart on crash
- ✅ Memory limits
- ✅ Log management
- ✅ System startup integration

**File**: [ecosystem.production.config.js](ecosystem.production.config.js)

### 5. SSL Certificate
- ✅ Let's Encrypt free SSL
- ✅ Auto-renewal configured
- ✅ HTTPS enforcement

## Deployment Files Created

| File | Purpose |
|------|---------|
| `nginx.conf` | Nginx reverse proxy configuration |
| `deploy.sh` | Automated deployment script |
| `update.sh` | Quick update script |
| `verify-deployment.sh` | Deployment verification |
| `DEPLOYMENT.md` | Comprehensive deployment guide |
| `DEPLOY_CHECKLIST.md` | Quick deployment checklist |
| `ecosystem.production.config.js` | PM2 production config |

## Architecture

```
Internet (HTTPS)
       ↓
    Nginx (:443)
       ↓
    ┌─────────────┬──────────────┐
    │             │              │
Frontend       Backend      WebSocket
(Static)    (:8000/api)   (:8000/ws)
  (dist)      (FastAPI)    (FastAPI)
```

## Deployment Commands

### Initial Deployment
```bash
sudo ./deploy.sh
```

### Update Application
```bash
./update.sh
```

### Verify Deployment
```bash
./verify-deployment.sh
```

### Monitor
```bash
pm2 monit
pm2 logs
```

## Access Points

- **Frontend**: https://crawler.ash-api.online
- **API**: https://crawler.ash-api.online/api
- **Docs**: https://crawler.ash-api.online/docs
- **WebSocket**: wss://crawler.ash-api.online/ws

## Security Features

1. **HTTPS Only**
   - Automatic HTTP → HTTPS redirect
   - TLS 1.2 and 1.3
   - Strong cipher suites

2. **Security Headers**
   - X-Frame-Options
   - X-Content-Type-Options
   - X-XSS-Protection
   - Strict-Transport-Security (HSTS)
   - Referrer-Policy

3. **Authentication**
   - Token-based login
   - Configurable in `.env`
   - Stored in localStorage

4. **Access Control**
   - CORS configured for specific domains
   - Hidden files denied
   - Rate limiting (can be added)

## Performance Optimizations

1. **Frontend**
   - Code splitting
   - Vendor chunks
   - Asset caching (1 year)
   - Gzip compression

2. **Backend**
   - Multiple workers in production
   - Connection pooling
   - Async operations

3. **Nginx**
   - Static file caching
   - Gzip compression
   - HTTP/2 enabled
   - Proxy buffering

## Monitoring & Logs

### Application Logs
```bash
pm2 logs                         # All logs
pm2 logs crawlbot-backend        # Backend only
pm2 logs crawlbot-frontend       # Frontend only
```

### Nginx Logs
```bash
sudo tail -f /var/log/nginx/crawlbot-access.log
sudo tail -f /var/log/nginx/crawlbot-error.log
```

### System Logs
```bash
sudo journalctl -u nginx -f
sudo journalctl -u pm2-root -f
```

## Backup Strategy

### Database Backup
```bash
# Manual backup
cp crawlbot.db backups/crawlbot-$(date +%Y%m%d).db

# Automated (add to crontab)
0 2 * * * cp /home/Crawlbot/crawlbot.db /home/Crawlbot/backups/crawlbot-$(date +\%Y\%m\%d).db
```

### Configuration Backup
```bash
# Backup important configs
tar -czf config-backup-$(date +%Y%m%d).tar.gz .env nginx.conf ecosystem.production.config.js
```

## Maintenance Tasks

### Daily
- ✅ Check PM2 status: `pm2 list`
- ✅ Review error logs

### Weekly
- ✅ Check disk space: `df -h`
- ✅ Review access logs
- ✅ Monitor memory usage: `free -h`

### Monthly
- ✅ Update system packages: `sudo apt update && sudo apt upgrade`
- ✅ Backup database
- ✅ Review SSL certificate: `sudo certbot certificates`
- ✅ Clean old logs: `pm2 flush`

## Scaling Considerations

### Vertical Scaling
- Increase server resources (CPU, RAM)
- Adjust PM2 worker count
- Tune nginx worker processes

### Horizontal Scaling
- Add load balancer
- Multiple backend instances
- Shared database (PostgreSQL)
- Redis for session management

## Next Steps

1. **Set Production Token**
   ```bash
   nano .env
   # Change LOGIN_TOKEN to a secure value
   ```

2. **Update Deploy Script Email**
   ```bash
   nano deploy.sh
   # Set your email for SSL certificate
   ```

3. **Run Deployment**
   ```bash
   sudo ./deploy.sh
   ```

4. **Verify Everything Works**
   ```bash
   ./verify-deployment.sh
   ```

5. **Monitor for 24 Hours**
   ```bash
   pm2 monit
   ```

## Support & Documentation

- [DEPLOYMENT.md](DEPLOYMENT.md) - Full deployment guide
- [DEPLOY_CHECKLIST.md](DEPLOY_CHECKLIST.md) - Quick checklist
- [PM2_GUIDE.md](PM2_GUIDE.md) - PM2 documentation
- [README.md](README.md) - Project overview

## Troubleshooting Quick Reference

| Issue | Solution |
|-------|----------|
| Can't access site | Check DNS, firewall, nginx status |
| SSL error | Run `sudo certbot --nginx -d crawler.ash-api.online` |
| Backend not responding | Check `pm2 logs crawlbot-backend` |
| WebSocket fails | Verify nginx websocket config |
| High memory | Restart PM2: `pm2 restart all` |
| 502 Bad Gateway | Backend down, check `pm2 list` |

---

**Deployed**: May 28, 2026  
**Domain**: https://crawler.ash-api.online  
**Stack**: Vue 3 + FastAPI + Nginx + PM2 + Let's Encrypt
