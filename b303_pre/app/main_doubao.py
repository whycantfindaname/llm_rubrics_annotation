# app/main.py

from fastapi import FastAPI
from .routes import router
from .middleware import logging_middleware

app = FastAPI()
app.include_router(router)
app.middleware("http")(logging_middleware)

@app.get("/")
def root():
    return {"message": "API is alive"}
