# app/middleware.py
import time
from fastapi import Request

async def logging_middleware(request: Request, call_next):
    # Exclude static files
    path = request.url.path
    if path.startswith("/static") or path.endswith(".html"):
        return await call_next(request)
    
    # Record start time
    start_time = time.perf_counter()
    
    # Process the request
    response = await call_next(request)
    
    # Calculate duration in milliseconds
    duration = (time.perf_counter() - start_time) * 1000
    
    # Log the request
    print(f"{request.method} {path} {response.status_code} {duration:.2f}ms")
    
    return response