"""FastAPI entry point.  Run with:  uvicorn app.main:app --reload"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .config import BASE_DIR
from .routes import router

app = FastAPI(title="FitBuddy - AI Fitness Plan Generator")

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
app.include_router(router)
