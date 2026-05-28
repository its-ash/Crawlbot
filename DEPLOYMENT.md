# Production Deployment Guide

## Prerequisites

- Ubuntu/Debian server with root access
- Domain name pointing to your server IP: `crawler.ash-api.online`
- Node.js 18+ and Python 3.9+ installed
- PM2 installed globally: `npm install -g pm2`

## Quick Deployment

### 1. Update Email in Deploy Script

Edit `deploy.sh` and change:
```bash
EMAIL="your-email@example.com"  # Change to your actual email
```

### 2. Run Deployment Script

```bash
sudo ./deploy.sh
```

This script will:
- ✅ Install and configure Nginx
- ✅ Build the frontend production bundle
- ✅ Obtain SSL certificate from Let's Encrypt
- ✅ Configure reverse proxy
- ✅ Start PM2 processes
- ✅ Setup auto-start on boot

## Manual Deployment

If you prefer manual setup:

### 1. Install Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Nginx and Certbot
sudo apt install -y nginx certbot python3-certbot-nginx

# Install PM2 and serve
npm install -g pm2 serve
```

### 2. Build Frontend

```bash
cd /home/Crawlbot/frontend
npm install
npm run build
cd ..
```

### 3. Configure Nginx

```bash
# Copy nginx config
sudo cp nginx.conf /etc/nginx/sites-available/crawlbot

# Enable site
sudo ln -s /etc/nginx/sites-available/crawlbot /etc/nginx/sites-enabled/crawlbot

# Remove default site
sudo rm /etc/nginx/sites-enabled/default

# Test configuration
sudo nginx -t

# Restart nginx
sudo systemctl restart nginx
sudo systemctl enable nginx
```

### 4. Obtain SSL Certificate

```bash
# Make sure DNS is pointing to your server first
sudo certbot --nginx -d crawler.ash-api.online --non-interactive --agree-tos -m your-email@example.com --redirect
```

### 5. Start Backend with PM2

```bash
cd /home/Crawlbot

# Create .env file if not exists
cp .env.example .env
# Edit .env and set your LOGIN_TOKEN

# Start PM2 processes
pm2 start ecosystem.production.config.js

# Save PM2 process list
pm2 save

# Setup auto-start on boot
pm2 startup systemd
# Run the command it shows
```

## DNS Configuration

Point your domain to your server:

```
Type: A Record
Name: crawler (or @)
Value: YOUR_SERVER_IP
TTL: 3600
```

Wait for DNS propagation (can take up to 48 hours, usually 5-30 minutes).

Verify DNS:
```bash
nslookup crawler.ash-api.online
# Should show your server IP
```

## Firewall Configuration

```bash
# Allow HTTP and HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 22/tcp  # SSH
sudo ufw enable

# Check status
sudo ufw status
```

## Environment Variables

Make sure `/home/Crawlbot/.env` contains:

```bash
# Authentication
LOGIN_TOKEN=your_secure_production_token

# Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3

# Database
DATABASE_URL=sqlite:///./crawlbot.db

# Search Engine (optional)
# GOOGLE_API_KEY=your_key
# GOOGLE_CSE_ID=your_cse_id

# Proxy (optional)
# PROXY_URL=http://proxy:port
```

## Verify Deployment

### 1. Check Services

```bash
# Check PM2 processes
pm2 list
pm2 logs

# Check Nginx
sudo systemctl status nginx

# Check SSL certificate
sudo certbot certificates
```

### 2. Test Application

Visit: `https://crawler.ash-api.online`

You should see:
- ✅ Login page
- ✅ HTTPS lock icon in browser
- ✅ No certificate warnings

### 3. Test Backend API

Visit: `https://crawler.ash-api.online/docs`

You should see the FastAPI documentation.

## SSL Certificate Auto-Renewal

Certbot automatically renews certificates. Test it:

```bash
sudo certbot renew --dry-run
```

If successful, renewal will happen automatically before expiration.

## Monitoring

### PM2 Monitoring

```bash
# Real-time monitoring
pm2 monit

# View logs
pm2 logs
pm2 logs crawlbot-backend
pm2 logs crawlbot-frontend

# Process info
pm2 info crawlbot-backend
```

### Nginx Logs

```bash
# Access logs
sudo tail -f /var/log/nginx/crawlbot-access.log

# Error logs
sudo tail -f /var/log/nginx/crawlbot-error.log
```

### System Resources

```bash
# Install htop
sudo apt install htop

# Monitor resources
htop
```

## Maintenance

### Update Application

```bash
cd /home/Crawlbot

# Pull latest changes (if using git)
git pull

# Update backend
source venv/bin/activate
pip install -r requirements.txt
deactivate

# Update and rebuild frontend
cd frontend
npm install
npm run build
cd ..

# Restart services
pm2 restart all

# Or reload without downtime
pm2 reload all
```

### Restart Services

```bash
# Restart PM2 processes
pm2 restart all

# Restart Nginx
sudo systemctl restart nginx

# Restart all
pm2 restart all && sudo systemctl restart nginx
```

### View Logs

```bash
# Application logs
pm2 logs --lines 100

# Nginx logs
sudo tail -n 100 /var/log/nginx/crawlbot-error.log
```

### Backup Database

```bash
# Create backup directory
mkdir -p /home/Crawlbot/backups

# Backup database
cp /home/Crawlbot/crawlbot.db /home/Crawlbot/backups/crawlbot-$(date +%Y%m%d-%H%M%S).db

# List backups
ls -lh /home/Crawlbot/backups/
```

## Troubleshooting

### Application Not Loading

1. Check PM2 processes:
   ```bash
   pm2 list
   pm2 logs
   ```

2. Check Nginx:
   ```bash
   sudo systemctl status nginx
   sudo nginx -t
   ```

3. Check firewall:
   ```bash
   sudo ufw status
   ```

### SSL Certificate Issues

```bash
# Check certificate status
sudo certbot certificates

# Force renewal
sudo certbot renew --force-renewal

# Check nginx config
sudo nginx -t
```

### Backend Not Responding

```bash
# Check if backend is running
pm2 list

# Check backend logs
pm2 logs crawlbot-backend --err

# Restart backend
pm2 restart crawlbot-backend

# Check if port 8000 is listening
sudo netstat -tlnp | grep 8000
```

### WebSocket Connection Issues

1. Check nginx websocket configuration
2. Check browser console for errors
3. Verify backend is running: `pm2 logs crawlbot-backend`

### High Memory Usage

```bash
# Check memory usage
free -h
pm2 monit

# Restart processes
pm2 restart all

# Adjust memory limits in ecosystem.production.config.js
```

## Security Checklist

- [x] HTTPS enabled with valid SSL certificate
- [x] Strong LOGIN_TOKEN set in .env
- [x] Firewall configured (UFW)
- [x] Nginx security headers enabled
- [x] SSH key authentication (recommended)
- [x] Regular system updates
- [x] Database backups scheduled
- [x] PM2 auto-restart enabled
- [x] Log rotation configured

## Performance Optimization

### 1. Enable Gzip in Nginx

Already configured in `nginx.conf` with compression for assets.

### 2. PM2 Cluster Mode (Optional)

For high traffic, edit `ecosystem.production.config.js`:

```javascript
instances: 'max',  // Use all CPU cores
exec_mode: 'cluster'
```

### 3. Database Optimization

For production with many agents, consider PostgreSQL:

```bash
# Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# Update DATABASE_URL in .env
DATABASE_URL=postgresql://user:pass@localhost/crawlbot
```

## Support

If you encounter issues:

1. Check logs: `pm2 logs` and `/var/log/nginx/`
2. Verify DNS: `nslookup crawler.ash-api.online`
3. Test SSL: `https://www.ssllabs.com/ssltest/`
4. Check firewall: `sudo ufw status`

## URLs

- **Application**: https://crawler.ash-api.online
- **API Docs**: https://crawler.ash-api.online/docs
- **API Base**: https://crawler.ash-api.online/api
