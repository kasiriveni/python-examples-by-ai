"""
Deployment: Gunicorn + Nginx configuration patterns.
Documents production WSGI server setup and Nginx reverse proxy.
"""
# ─────────────────────────────────────────────────────────
# GUNICORN CONFIGURATION (gunicorn.conf.py)
# ─────────────────────────────────────────────────────────
GUNICORN_CONFIG = """
# gunicorn.conf.py
# Run: gunicorn -c gunicorn.conf.py myapp:app

import multiprocessing
import os

# ── Workers ──────────────────────────────
workers = multiprocessing.cpu_count() * 2 + 1   # recommended formula
worker_class = "uvicorn.workers.UvicornWorker"  # for ASGI (FastAPI)
# worker_class = "sync"                          # for WSGI (Flask/Django)
threads = 2                                      # threads per worker (sync only)
worker_connections = 1000                        # max simultaneous clients (async)

# ── Binding ──────────────────────────────
bind = "0.0.0.0:8000"
backlog = 2048

# ── Timeouts ─────────────────────────────
timeout = 30            # kill unresponsive workers
keepalive = 2           # persistent TCP connection keep-alive
graceful_timeout = 30   # wait for requests to finish on shutdown

# ── Logging ──────────────────────────────
loglevel = "info"
accesslog = "-"         # stdout
errorlog  = "-"         # stdout
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" in %(D)sµs'

# ── Process Naming ────────────────────────
proc_name = "myapp"

# ── Security ─────────────────────────────
limit_request_line   = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# ── Hooks ────────────────────────────────
def on_starting(server):
    print("Starting Gunicorn...")

def on_exit(server):
    print("Gunicorn stopped.")

def worker_exit(server, worker):
    print(f"Worker {worker.pid} exited.")

def post_fork(server, worker):
    # Reset any connections forked from parent
    # e.g., db.engine.dispose()
    pass
"""

# ─────────────────────────────────────────────────────────
# NGINX REVERSE PROXY CONFIG
# ─────────────────────────────────────────────────────────
NGINX_CONFIG = """
# /etc/nginx/sites-available/myapp
# ln -s /etc/nginx/sites-available/myapp /etc/nginx/sites-enabled/

upstream app_servers {
    least_conn;                          # load balancing strategy
    server 127.0.0.1:8000 weight=3;
    server 127.0.0.1:8001 weight=1;
    keepalive 32;                        # keep connections warm
}

server {
    listen 80;
    server_name example.com www.example.com;
    return 301 https://$server_name$request_uri;  # redirect to HTTPS
}

server {
    listen 443 ssl http2;
    server_name example.com www.example.com;

    # ── SSL ──────────────────────────────
    ssl_certificate     /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers 'ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # ── Security Headers ─────────────────
    add_header Strict-Transport-Security "max-age=63072000; includeSubDomains" always;
    add_header X-Content-Type-Options nosniff;
    add_header X-Frame-Options DENY;
    add_header X-XSS-Protection "1; mode=block";
    add_header Referrer-Policy "strict-origin-when-cross-origin";

    # ── Rate Limiting ─────────────────────
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req zone=api burst=20 nodelay;

    # ── Gzip ─────────────────────────────
    gzip on;
    gzip_types text/plain application/json application/javascript text/css;
    gzip_min_length 1024;
    gzip_proxied any;

    # ── Static Files ──────────────────────
    location /static/ {
        alias /var/www/myapp/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias /var/www/myapp/media/;
        expires 7d;
    }

    # ── API / App ─────────────────────────
    location / {
        proxy_pass http://app_servers;
        proxy_http_version 1.1;

        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Connection        "";

        proxy_read_timeout   60s;
        proxy_connect_timeout 5s;
        proxy_send_timeout   60s;
        proxy_buffering      on;
        proxy_buffer_size    16k;
        proxy_buffers        4 32k;
    }

    # ── Websocket support ─────────────────
    location /ws/ {
        proxy_pass http://app_servers;
        proxy_http_version 1.1;
        proxy_set_header Upgrade    $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host       $host;
        proxy_read_timeout 3600s;
    }
}
"""

# ─────────────────────────────────────────────────────────
# SYSTEMD SERVICE
# ─────────────────────────────────────────────────────────
SYSTEMD_SERVICE = """
# /etc/systemd/system/myapp.service
# systemctl enable myapp && systemctl start myapp

[Unit]
Description=MyApp Gunicorn Service
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/var/www/myapp
Environment="PATH=/var/www/myapp/.venv/bin"
EnvironmentFile=/var/www/myapp/.env
ExecStart=/var/www/myapp/.venv/bin/gunicorn -c gunicorn.conf.py myapp:app
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=30
PrivateTmp=true
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
"""

# ─────────────────────────────────────────────────────────
# HEALTH CHECK ENDPOINT (FastAPI example)
# ─────────────────────────────────────────────────────────
HEALTH_CHECK = '''
from fastapi import FastAPI, status
from pydantic import BaseModel
import time, os

app = FastAPI()
START_TIME = time.time()

class HealthResponse(BaseModel):
    status: str
    uptime: float
    version: str

@app.get("/health", response_model=HealthResponse)
def health():
    return HealthResponse(
        status="ok",
        uptime=round(time.time() - START_TIME, 2),
        version=os.getenv("APP_VERSION", "unknown"),
    )

@app.get("/ready", status_code=status.HTTP_200_OK)
def readiness():
    """Kubernetes readiness probe: verify DB, cache are accessible."""
    # check_db(); check_redis()  — add real checks here
    return {"ready": True}

@app.get("/live", status_code=status.HTTP_200_OK)
def liveness():
    """Kubernetes liveness probe: is the process alive?"""
    return {"alive": True}
'''

if __name__ == "__main__":
    print("=== Gunicorn Configuration ===")
    print(GUNICORN_CONFIG[:500] + "...\n")

    print("=== Nginx Configuration ===")
    print(NGINX_CONFIG[:500] + "...\n")

    print("=== Systemd Service ===")
    print(SYSTEMD_SERVICE.strip())

    print("\n=== Health Check Endpoint ===")
    print(HEALTH_CHECK.strip())
