"""
Logger Configuration
--------------------
Sets up application-wide logging with console and file handlers, including log rotation.

Features:
- Logs to both console and file (rotated daily, keeps 30 days)
- Custom log format with timestamp, level, and message
- Ensures log directory exists
- Avoids duplicate handlers

Usage:
Import the logger object and use logger.info(), logger.error(), etc. throughout the app.
"""

# common/logger.py

import logging
import os
from logging.handlers import TimedRotatingFileHandler

# Create logger
logger = logging.getLogger("fastapi_app")
logger.setLevel(logging.INFO)

# Log format
formatter = logging.Formatter("[%(asctime)s] - %(levelname)s - %(message)s")

# Console logging
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# Log file directory
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

# File logging with rotation — 1 file/day, keep 30 days
file_handler = TimedRotatingFileHandler(
    filename=os.path.join(log_dir, "app.log"),
    when="midnight",
    interval=1,
    backupCount=30,
    encoding="utf-8"
)
file_handler.setFormatter(formatter)
file_handler.suffix = "%Y-%m-%d"  # adds date suffix to rotated logs

# Avoid duplicate handlers
if not logger.hasHandlers():
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
