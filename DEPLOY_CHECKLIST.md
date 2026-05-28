# Quick Deployment Checklist

## Pre-Deployment

- [ ] Server running Ubuntu/Debian
- [ ] Root/sudo access
- [ ] Node.js 18+ installed: `node --version`
- [ ] Python 3.9+ installed: `python3 --version`
- [ ] PM2 installed: `npm install -g pm2`
- [ ] Domain DNS pointing to server IP
- [ ] Ports 80, 443 open in firewall

## Deployment Steps

1. **Update deploy script email**
   ```bash
   nano deploy.sh
   # Change: EMAIL="your-email@example.com"
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   nano .env
   # Set: LOGIN_TOKEN=your_secure_token
   ```

3. **Run deployment**
   ```bash
   sudo ./deploy.sh
   ```

4. **Verify**
   - [ ] Visit: https://crawler.ash-api.online
   - [ ] Login with your token
   - [ ] Create test agent
   - [ ] Check PM2: `pm2 list`
   - [ ] Check logs: `pm2 logs`

## Post-Deployment

- [ ] SSL certificate obtained
- [ ] Application accessible via HTTPS
- [ ] PM2 processes running
- [ ] Auto-restart on boot enabled
- [ ] Change default LOGIN_TOKEN
- [ ] Setup database backups
- [ ] Configure monitoring

## Quick Commands

```bash
# Status
pm2 list
sudo systemctl status nginx

# Logs
pm2 logs
sudo tail -f /var/log/nginx/crawlbot-error.log

# Restart
pm2 restart all
sudo systemctl restart nginx

# Update
./update.sh

# Monitor
pm2 monit
```

## Troubleshooting

**Can't access site:**
1. Check PM2: `pm2 list`
2. Check Nginx: `sudo systemctl status nginx`
3. Check DNS: `nslookup crawler.ash-api.online`
4. Check firewall: `sudo ufw status`

**SSL certificate failed:**
```bash
sudo certbot --nginx -d crawler.ash-api.online
```

**Backend not responding:**
```bash
pm2 logs crawlbot-backend
pm2 restart crawlbot-backend
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for full documentation.
