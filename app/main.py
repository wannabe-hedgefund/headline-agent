from fastapi import FastAPI
from python_utils.logging.logging import init_logger

from app.api.v1.router import api_router

# initialize logger
logger = init_logger()

logger.info("Starting application...")

# initialize FastAPI
app = FastAPI()

# Connect routers to application
app.include_router(api_router, prefix="/v1")