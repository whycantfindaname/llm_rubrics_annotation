# app/main.py

from fastapi import FastAPI
from .middleware import logging_middleware
from .routes import router

app = FastAPI()
app.middleware("http")(logging_middleware)
app.include_router(router)

@app.get("/")
def root():
    return {"message": "API is alive"}
