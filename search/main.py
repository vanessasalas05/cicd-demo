from typing import Union

from fastapi import FastAPI
from query import search_query

app = FastAPI()

@app.post("/search")
def search(question: str):
    return {"answer": search_query(question)}