from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os
from .routers.optimize import router as optimize_router
from .routers.crud import router as crud_router

app = FastAPI(title="AI Study Planner (GA)")

app.include_router(crud_router, prefix="/api")
app.include_router(optimize_router, prefix="/api")

_frontend_dir = os.path.join(os.path.dirname(__file__), "..", "frontend")
app.mount("/", StaticFiles(directory=os.path.abspath(_frontend_dir), html=True), name="frontend")