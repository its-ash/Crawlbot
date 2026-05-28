# PM2 Process Management Guide

## Installation

```bash
# Install PM2 globally
npm install -g pm2

# For production, also install serve for frontend
npm install -g serve
```

## Development Mode

### Start All Services
```bash
# Create logs directory
mkdir -p logs

# Start both backend and frontend
pm2 start ecosystem.config.js

# Or start individually
pm2 start ecosystem.config.js --only crawlbot-backend
pm2 start ecosystem.config.js --only crawlbot-frontend
```

### Monitor Services
```bash
# View all processes
pm2 list

# Monitor in real-time
pm2 monit

# View logs
pm2 logs
pm2 logs crawlbot-backend
pm2 logs crawlbot-frontend

# View logs in real-time with filtering
pm2 logs --lines 100
```

### Manage Services
```bash
# Restart services
pm2 restart all
pm2 restart crawlbot-backend
pm2 restart crawlbot-frontend

# Stop services
pm2 stop all
pm2 stop crawlbot-backend

# Delete services
pm2 delete all
pm2 delete crawlbot-backend
```

## Production Mode

### Build and Deploy
```bash
# Build frontend
cd frontend
npm run build
cd ..

# Start production services
pm2 start ecosystem.production.config.js

# Save PM2 process list
pm2 save

# Setup PM2 to start on system boot
pm2 startup
# Follow the instructions shown
```

### Production Commands
```bash
# Reload without downtime
pm2 reload all

# Scale instances (if needed)
pm2 scale crawlbot-backend 4

# Monitor production
pm2 monit
```

## Advanced Usage

### Environment-Specific Configurations
```bash
# Start with custom environment
pm2 start ecosystem.config.js --env production

# Start with specific config
pm2 start ecosystem.production.config.js
```

### Log Management
```bash
# Flush logs
pm2 flush

# Rotate logs (install module first)
pm2 install pm2-logrotate

# Configure log rotation
pm2 set pm2-logrotate:max_size 10M
pm2 set pm2-logrotate:retain 7
pm2 set pm2-logrotate:compress true
```

### Process Inspection
```bash
# Detailed process info
pm2 info crawlbot-backend

# CPU and memory profiling
pm2 profile:cpu <process_id> 10
pm2 profile:mem <process_id> 10
```

## Troubleshooting

### Backend Won't Start
```bash
# Check if virtual environment exists
ls -la venv/bin/uvicorn

# Manually test backend
source venv/bin/activate
uvicorn backend.main:app --host 0.0.0.0 --port 8000

# Check PM2 logs
pm2 logs crawlbot-backend --err
```

### Frontend Won't Start
```bash
# Check if node_modules installed
cd frontend && npm install

# Manually test frontend
cd frontend && npm run dev

# Check PM2 logs
pm2 logs crawlbot-frontend --err
```

### Port Already in Use
```bash
# Find and kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Find and kill process on port 5173
lsof -ti:5173 | xargs kill -9

# Restart PM2 services
pm2 restart all
```

## Auto-Start on System Boot

### Linux/macOS
```bash
# Save current process list
pm2 save

# Generate startup script
pm2 startup

# Copy and run the command shown

# Verify
pm2 list
```

### Disable Auto-Start
```bash
pm2 unstartup
```

## Useful Aliases

Add to your `.bashrc` or `.zshrc`:

```bash
alias pm2-start='pm2 start ecosystem.config.js'
alias pm2-restart='pm2 restart all'
alias pm2-stop='pm2 stop all'
alias pm2-logs='pm2 logs --lines 50'
alias pm2-status='pm2 list'
```

## Production Checklist

- [ ] Build frontend: `cd frontend && npm run build`
- [ ] Install PM2: `npm install -g pm2`
- [ ] Install serve: `npm install -g serve`
- [ ] Create logs directory: `mkdir -p logs`
- [ ] Set environment variables in `.env`
- [ ] Start production: `pm2 start ecosystem.production.config.js`
- [ ] Save process list: `pm2 save`
- [ ] Setup auto-start: `pm2 startup`
- [ ] Install log rotation: `pm2 install pm2-logrotate`
- [ ] Test access: Visit http://your-server:5173

## Monitoring with PM2 Plus (Optional)

```bash
# Connect to PM2 Plus for advanced monitoring
pm2 link <secret_key> <public_key>

# Features:
# - Real-time monitoring
# - Email alerts
# - Custom metrics
# - Remote actions
```
