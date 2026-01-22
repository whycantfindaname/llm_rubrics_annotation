# app/models.py

from pydantic import BaseModel

class Item(BaseModel):
    name: str
    quantity: int
