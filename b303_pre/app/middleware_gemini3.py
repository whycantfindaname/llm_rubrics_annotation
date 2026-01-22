import time
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000
        
        path = request.url.path
        if not (path.startswith("/static") or path.endswith(".html")):
            print(f"{request.method} {path} {response.status_code} {process_time:.2f}ms")
            
        return response
