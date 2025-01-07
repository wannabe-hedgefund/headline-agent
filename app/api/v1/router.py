''' consolidates all v1 routers to a single router '''

from fastapi import APIRouter
from app.api.v1.endpoints import headline, web_scraper

api_router = APIRouter()

# Load all endpoints
api_router.include_router(headline.router, prefix="/headline")
api_router.include_router(web_scraper.router, prefix="/web-scraper")