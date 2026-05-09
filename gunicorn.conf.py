import multiprocessing

# Gunicorn configuration file
bind = "0.0.0.0:80"
workers = multiprocessing.cpu_count() * 2 + 1
timeout = 120  # TTS generation can take time
accesslog = "-" # Log to stdout
errorlog = "-"  # Log to stderr
