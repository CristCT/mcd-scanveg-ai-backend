import os

# Configuración de gunicorn para Render

# Bind - Puerto dinámico de Render
bind = f"0.0.0.0:{os.environ.get('PORT', 5000)}"

# Workers - Número de procesos worker
workers = int(os.environ.get('WEB_CONCURRENCY', 2))

# Worker class
worker_class = "sync"

# Worker connections
worker_connections = 1000

# Timeout
timeout = 120
keepalive = 2

# Preload app
preload_app = True

# Max requests per worker
max_requests = 1000
max_requests_jitter = 100

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = "mcd_scanveg_backend"

# Graceful timeout
graceful_timeout = 30

# Temporary directory
tmp_upload_dir = None

# Security
forwarded_allow_ips = "*"
secure_scheme_headers = {
    'X-FORWARDED-PROTOCOL': 'ssl',
    'X-FORWARDED-PROTO': 'https',
    'X-FORWARDED-SSL': 'on'
}