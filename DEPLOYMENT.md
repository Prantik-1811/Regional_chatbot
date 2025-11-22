# Deployment Guide - Cyber Intelligence Chatbot

This guide provides step-by-step instructions for deploying the Cyber Intelligence Chatbot as a production website using Docker.

## Architecture

The deployment uses a three-tier architecture:
- **Nginx Reverse Proxy** (Public-facing on ports 80/443)
- **Frontend** (React SPA, internal only)
- **Backend API** (FastAPI, internal only)

All services communicate via internal Docker networks. Only nginx is exposed to the internet.

## Prerequisites

1. **Docker & Docker Compose**
   - Install Docker: https://docs.docker.com/get-docker/
   - Docker Compose is included with Docker Desktop

2. **Server Requirements (for AI)**
   - **Minimum**: 4 CPU cores, 8GB RAM (Responses ~30-60s)
   - **Recommended**: GPU-enabled server (Responses <5s)
   - **Disk**: 30GB disk space (for Docker images + AI models)

3. **Domain Name** (Optional but recommended for production)
   - Configure DNS A record pointing to your server's IP

## Quick Start (HTTP Only)

Perfect for testing or local deployment:

```bash
# Navigate to project directory
cd "d:\Cyber Warrior\Chatbot"

# Build and start all services
docker-compose up -d

# ⚠️ IMPORTANT: Pull the AI Model (Run once)
# This downloads the Llama 3.2 model (approx 2GB) into the container
docker exec chatbot-ollama ollama pull llama3.2

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

Access the chatbot at: `http://your-server-ip` or `http://localhost`

> [!NOTE]
> **First Response Delay**: The first time you ask a question, it might take 1-2 minutes as the model loads into memory.
> **Nginx Timeout**: The configuration has a **300s (5 minute)** timeout to allow for slower CPU-based AI generation.

Access the chatbot at: `http://your-server-ip` or `http://localhost`

## Production Deployment (HTTPS)

### Step 1: Obtain SSL Certificate

**Option A: Let's Encrypt (Recommended)**

```bash
# Install certbot
sudo apt-get update
sudo apt-get install certbot

# Obtain certificate
sudo certbot certonly --standalone -d your-domain.com
```

Certificates will be saved to `/etc/letsencrypt/live/your-domain.com/`

**Option B: Use Existing Certificate**

Place your certificate files in `./ssl/`:
- `cert.pem` - SSL certificate
- `key.pem` - Private key

### Step 2: Configure Nginx for HTTPS

Edit `nginx/nginx.conf` and uncomment the HTTPS server block:

```nginx
server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    # ... rest of configuration
}
```

### Step 3: Update docker-compose.yml

Uncomment the SSL volume mount in `docker-compose.yml`:

```yaml
nginx:
  volumes:
    - ./ssl:/etc/nginx/ssl:ro
```

### Step 4: Deploy

```bash
docker-compose down
docker-compose up -d --build
```

Access at: `https://your-domain.com`

## Deployment on Any Server

These steps work on **any** Linux server (Ubuntu/Debian recommended) that has Docker installed.

1. **Connect to your server**
   ```bash
   ssh user@your-server-ip
   ```

2. **Install Docker & Docker Compose**
   ```bash
   # Download and run the official installation script
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   ```

3. **Deploy the Chatbot**
   ```bash
   # Clone your repository (or upload files via SFTP)
   git clone your-repo-url
   cd Chatbot
   
   # Start the application
   docker-compose up -d
   
   # ⚠️ IMPORTANT: Pull the AI Model
   docker exec chatbot-ollama ollama pull llama3.2
   ```

## Management Commands

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f nginx
```

### Restart Services
```bash
# Restart all
docker-compose restart

# Restart specific service
docker-compose restart backend
```

### Stop Services
```bash
docker-compose stop
```

### Remove Everything
```bash
docker-compose down -v  # -v removes volumes too
```

### Update Application
```bash
# Pull latest code
git pull

# Rebuild and restart
docker-compose up -d --build
```

## Backup and Restore

### Backup ChromaDB Data
```bash
# Create backup
docker run --rm -v chatbot_chroma_db_data:/data -v $(pwd):/backup \
  ubuntu tar czf /backup/chroma_backup_$(date +%Y%m%d).tar.gz /data

# Backup is saved as: chroma_backup_YYYYMMDD.tar.gz
```

### Restore ChromaDB Data
```bash
# Stop services
docker-compose down

# Restore backup
docker run --rm -v chatbot_chroma_db_data:/data -v $(pwd):/backup \
  ubuntu tar xzf /backup/chroma_backup_YYYYMMDD.tar.gz -C /

# Restart services
docker-compose up -d
```

## Monitoring

### Check Resource Usage
```bash
docker stats
```

### Health Checks
```bash
# Nginx health
curl http://localhost/health

# Backend health
docker-compose exec backend curl http://localhost:8000/

# Check all containers
docker-compose ps
```

## Troubleshooting

### Container Won't Start
```bash
# Check logs
docker-compose logs backend

# Check if ports are in use
sudo netstat -tulpn | grep :80
sudo netstat -tulpn | grep :443
```

### Backend Connection Issues
```bash
# Verify backend is running
docker-compose exec backend curl http://localhost:8000/

# Check network connectivity
docker network ls
docker network inspect chatbot_backend_network
```

### ChromaDB Data Not Persisting
```bash
# Verify volume exists
docker volume ls | grep chroma

# Inspect volume
docker volume inspect chatbot_chroma_db_data
```

### SSL Certificate Issues
```bash
# Verify certificate files
docker-compose exec nginx ls -la /etc/nginx/ssl/

# Test nginx configuration
docker-compose exec nginx nginx -t
```

### 504 Gateway Timeout
If you see "Error: Request failed with status code 504":
1. **Cause**: The AI model is taking too long to generate a response (common on CPU).
2. **Fix**: The `nginx.conf` is already configured with a **300s timeout**.
3. **Action**: Ensure you are using the latest nginx image:
   ```bash
   docker-compose build nginx
   docker-compose up -d nginx
   ```

### 504 Gateway Timeout
If you see "Error: Request failed with status code 504":
1. **Cause**: The AI model is taking too long to generate a response (common on CPU).
2. **Fix**: The `nginx.conf` is already configured with a **300s timeout**.
3. **Action**: Ensure you are using the latest nginx image:
   ```bash
   docker-compose build nginx
   docker-compose up -d nginx
   ```

## Security Best Practices

1. **Use HTTPS in Production** - Always use SSL/TLS certificates
2. **Keep Docker Updated** - Regularly update Docker and images
3. **Limit Exposed Ports** - Only expose ports 80 and 443
4. **Use Firewall** - Configure UFW or cloud provider firewall
5. **Regular Backups** - Backup ChromaDB data regularly
6. **Monitor Logs** - Set up log monitoring and alerts
7. **Update Dependencies** - Keep Python and Node packages updated

## Performance Optimization

### Increase Worker Processes
Edit `backend/Dockerfile` to add more uvicorn workers:
```dockerfile
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

### Enable Nginx Caching
Add to `nginx/nginx.conf`:
```nginx
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=api_cache:10m max_size=100m;
```

### Scale Services
```bash
# Run multiple backend instances
docker-compose up -d --scale backend=3
```

## Support

For issues or questions:
- Check logs: `docker-compose logs -f`
- Review this guide
- Check Docker documentation: https://docs.docker.com/

## Next Steps

After deployment:
1. Test all functionality thoroughly
2. Set up monitoring and alerts
3. Configure automated backups
4. Set up SSL certificate auto-renewal (Let's Encrypt)
5. Implement CI/CD pipeline for updates
