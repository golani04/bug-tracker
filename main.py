from fastapi import FastAPI
from backend.api import api_router

app = FastAPI(title="Bug tracker")
app.include_router(api_router, prefix="/api")
