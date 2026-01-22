# app/main.py

from fastapi import FastAPI
from .routes import router
from .middleware import LoggingMiddleware

app = FastAPI()
app.add_middleware(LoggingMiddleware)
app.include_router(router)

@app.get("/")
def root():
    return {"message": "API is alive"}
