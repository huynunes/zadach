import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.db import Base, engine
from app.routes import analyze, history

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(name)s | %(message)s")
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting AI Text Assistant API...")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created/verified successfully.")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
    yield
    logger.info("Shutting down API...")

app = FastAPI(title="AI Text Assistant API", version="1.0.0", lifespan=lifespan)

@app.get("/health")
async def health_check():
    return {"status": "ok"}

app.include_router(analyze.router)
app.include_router(history.router)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=400, content={"detail": "Invalid JSON or empty text"})

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {exc}")
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})