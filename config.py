# Gunicorn config params
bind = "0.0.0.0:5000"
workers = 1
timeout = 1200
proc_name = 'gunicorn.proc'
pidfile = '/tmp/gunicorn.pid'
logfile = '/var/log/gunicorn/debug.log'
loglevel = 'debug'
errorlog = '/var/log/gunicorn/error.log'
accesslog = '/var/log/gunicorn/access.log'
max_requests = 10000  # kill worker after max requests
# DEBUG = True
