# common/logging_middleware.py

import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from common.logger import logger

class LoggingMiddleware(BaseHTTPMiddleware):
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
