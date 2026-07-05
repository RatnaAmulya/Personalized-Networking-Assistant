import logging
from fastapi import FastAPI, Request
import time

from app.routers import conversation

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("app.main")

# Initialize FastAPI app with OpenAPI documentation metadata
app = FastAPI(
    title="Personalized Networking Assistant",
    description="An AI-powered assistant for generating personalized networking conversation starters and fact-checking topics.",
    version="1.0.0"
)

# Middleware to log API execution details (request path, method, status code, processing time)
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    method = request.method
    path = request.url.path
    
    # Log incoming request info
    logger.info(f"Incoming request: {method} {path}")
    
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(f"Request completed: {method} {path} - Status: {response.status_code} - Process Time: {process_time:.4f}s")
        return response
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(f"Request failed: {method} {path} - Error: {e} - Process Time: {process_time:.4f}s")
        raise e

# Include routers
app.include_router(conversation.router, tags=["Conversation"])

# Welcome endpoint /
@app.get("/")
async def read_root():
    """
    Root endpoint serving a welcome message and confirming backend status.
    """
    return {
        "message": "Welcome to the Personalized Networking Assistant API! Go to /docs for Swagger API documentation.",
        "status": "online"
    }
