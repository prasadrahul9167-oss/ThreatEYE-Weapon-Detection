# ThreatEYE - Deployment Guide

## Deployment Options

### 1. Local Development

See [SETUP_GUIDE.md](docs/SETUP_GUIDE.md) for local setup instructions.

### 2. Docker Deployment

#### Create Dockerfile for Backend

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY server.py .

EXPOSE 8001

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8001"]
```

#### Create Dockerfile for Frontend

```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package.json yarn.lock ./
RUN yarn install --frozen-lockfile

COPY . .

EXPOSE 3000

CMD ["yarn", "start"]
```

#### Docker Compose

```yaml
version: '3.8'

services:
  mongodb:
    image: mongo:latest
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db

  backend:
    build: ./backend
    ports:
      - "8001:8001"
    environment:
      - MONGO_URL=mongodb://mongodb:27017
      - DB_NAME=threat_eye
      - CORS_ORIGINS=http://localhost:3000
    depends_on:
      - mongodb

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_BACKEND_URL=http://localhost:8001
    depends_on:
      - backend

volumes:
  mongodb_data:
```

#### Deploy with Docker

```bash
# Build and start
docker-compose up -d

# Check logs
docker-compose logs -f

# Stop
docker-compose down
```

### 3. Cloud Deployment

#### AWS (EC2)

1. Launch EC2 instance (Ubuntu 22.04)
2. Install dependencies (Python, Node.js, MongoDB)
3. Clone repository
4. Run setup script
5. Configure security groups (ports 3000, 8001)
6. Use PM2 or systemd for process management

#### Heroku

**Backend:**
```bash
heroku create threateye-backend
heroku addons:create mongolab
git subtree push --prefix backend heroku main
```

**Frontend:**
```bash
heroku create threateye-frontend
heroku config:set REACT_APP_BACKEND_URL=https://threateye-backend.herokuapp.com
git subtree push --prefix frontend heroku main
```

#### DigitalOcean

1. Create droplet (Ubuntu)
2. Install Docker
3. Use docker-compose for deployment
4. Configure firewall
5. Set up reverse proxy (Nginx)

#### Google Cloud Platform

1. Create VM instance
2. Install dependencies
3. Deploy application
4. Configure Cloud SQL (MongoDB Atlas alternative)
5. Set up Load Balancer

### 4. Kubernetes Deployment

#### Backend Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: threateye-backend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: threateye-backend
  template:
    metadata:
      labels:
        app: threateye-backend
    spec:
      containers:
      - name: backend
        image: threateye-backend:latest
        ports:
        - containerPort: 8001
        env:
        - name: MONGO_URL
          valueFrom:
            secretKeyRef:
              name: threateye-secrets
              key: mongo-url
```

#### Frontend Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: threateye-frontend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: threateye-frontend
  template:
    metadata:
      labels:
        app: threateye-frontend
    spec:
      containers:
      - name: frontend
        image: threateye-frontend:latest
        ports:
        - containerPort: 3000
```

### 5. Production Considerations

#### Security

- Use HTTPS (SSL/TLS certificates)
- Implement rate limiting
- Add authentication/authorization
- Sanitize user inputs
- Use environment variables for secrets
- Enable CORS properly
- Regular security audits

#### Performance

- Use CDN for static assets
- Implement caching (Redis)
- Optimize images and models
- Use load balancer
- Enable gzip compression
- Monitor resource usage

#### Monitoring

- Set up logging (CloudWatch, Datadog)
- Error tracking (Sentry)
- Performance monitoring (New Relic)
- Uptime monitoring (Pingdom)
- Database monitoring

#### Backup

- Regular database backups
- Automated backup scripts
- Test restore procedures
- Store backups offsite

#### Scaling

- Horizontal scaling (multiple instances)
- Vertical scaling (larger instances)
- Database replication
- Caching layer
- CDN for static content

### 6. Environment Variables

#### Production Backend (.env)

```env
MONGO_URL=mongodb://production-server:27017
DB_NAME=threateye_production
CORS_ORIGINS=https://yourdomain.com
ENVIRONMENT=production
LOG_LEVEL=INFO
```

#### Production Frontend (.env)

```env
REACT_APP_BACKEND_URL=https://api.yourdomain.com
REACT_APP_ENVIRONMENT=production
```

### 7. CI/CD Pipeline

#### GitHub Actions Example

```yaml
name: Deploy ThreatEYE

on:
  push:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: |
          cd backend && python -m pytest
          cd ../frontend && yarn test

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to production
        run: |
          # Your deployment script here
```

### 8. SSL/HTTPS Setup

#### Using Let's Encrypt (Free)

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal
sudo certbot renew --dry-run
```

#### Nginx Configuration

```nginx
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    location /api {
        proxy_pass http://localhost:8001;
    }

    location / {
        proxy_pass http://localhost:3000;
    }
}
```

### 9. Health Checks

Implement health check endpoints:

```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }
```

### 10. Rollback Strategy

- Keep previous version artifacts
- Use blue-green deployment
- Implement feature flags
- Test rollback procedures
- Monitor after deployment

---

For questions about deployment, check the documentation or open an issue.
