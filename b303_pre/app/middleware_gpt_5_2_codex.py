from time import perf_counter

from fastapi import Request


async def logging_middleware(request: Request, call_next):
    start_time = perf_counter()
    response = await call_next(request)
    duration_ms = (perf_counter() - start_time) * 1000
    path = request.url.path
    is_static = path.startswith("/static") or path.endswith(".html")
    if not is_static:
        print(f"{request.method} {path} {response.status_code} {duration_ms:.2f}ms")
    return response
