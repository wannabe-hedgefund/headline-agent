''' Web scraper code '''

from fastapi import APIRouter, HTTPException
from python_utils.logging.logging import init_logger
from bs4 import BeautifulSoup

import httpx
import asyncio

from app.schemas.web_scraper import WebScraperConfig
from app import paths

# Initialize logger
logger = init_logger()

# Initialize the router
router = APIRouter()

# Initialize the configs
web_scraper_config = WebScraperConfig.from_yaml(paths.WEB_SCRAPER_CONFIG_DIR)

''' API '''
@router.get('/scrape')
async def scrape(ticker: str):
    '''
    Description: Scrapes yahoo finance for news articles

    Step 1: Search website and scrape using the ticker
    Step 1.1: Validate that it's a valid ticker by checking it found articles
    Step 2: Parse and extract article headlines

    Args:
        ticker (str): ticker of stock that we're scraping for
    
    Return:
        TBD
    '''

    ''' Step 1: Fetch page '''
    # yahoo_finance_url = web_scraper_config.base_url.format(ticker=ticker)

    # try:
    #     async with httpx.AsyncClient(timeout=web_scraper_config.timeout) as client:
    #         logger.info(f'Calling {yahoo_finance_url}')
    #         response = await client.get(url=yahoo_finance_url, headers=web_scraper_config.headers)
    #         response.raise_for_status()
    #         # return response.text

    # except httpx.HTTPError as e:
    #     raise HTTPException(
    #         status_code=503,
    #         detail=f"Failed to fetch news: {str(e)}"
    #     )
    
    # return {"message": "test"}
