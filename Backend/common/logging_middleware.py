"""
Logging Middleware
------------------
Provides a FastAPI middleware class for logging incoming requests and responses.

Features:
- Logs request method and path
- Logs response status and duration
- Logs exceptions during request handling

Class:
- LoggingMiddleware: Middleware for logging HTTP requests and responses
"""

# common/logging_middleware.py

import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from common.logger import logger

class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to log incoming HTTP requests and responses.
    
    Methods:
        dispatch(request, call_next): Logs request details, handles exceptions, and logs response status and duration.
    """
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        logger.info(f"Incoming request: {request.method} {request.url.path}")

        try:
            response = await call_next(request)
        except Exception as e:
            logger.exception(f"Exception during request: {e}")
            raise

        duration = time.time() - start_time
        logger.info(
            f"Completed {request.method} {request.url.path} "
            f"with status {response.status_code} in {duration:.2f}s"
        )

        return response
