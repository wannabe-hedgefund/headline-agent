''' Web scraper code '''

from fastapi import APIRouter, HTTPException
from python_utils.logging.logging import init_logger
from bs4 import BeautifulSoup

import httpx
import asyncio
import requests

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
    agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15'
    headers = {'User-Agent': agent}
    url = 'https://finance.yahoo.com/quote/AAPL/news'
    data = requests.get(url, headers=headers)
    soup = BeautifulSoup(data.text, features="lxml")

    headline = soup.findAll('h3', class_='clamp yf-18q3fnf', limit=None)

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
