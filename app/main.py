from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routes import router

app = FastAPI(title="FitBuddy - AI Fitness Plan Generator")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(router)
