# Gunicorn configuration for Render
bind = "0.0.0.0:10000"
workers = 1
worker_class = "sync"
worker_connections = 1000
timeout = 300  # 5 minutes
keepalive = 2
max_requests = 1000
max_requests_jitter = 100
preload_app = True