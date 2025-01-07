''' Web scraper code '''

from fastapi import APIRouter, HTTPException
from python_utils.logging.logging import init_logger
from bs4 import BeautifulSoup

import httpx

from app.schemas.web_scraper import WebScraperConfig, WebScraperResponse
from app import paths

# Initialize logger
logger = init_logger()

# Initialize the router
router = APIRouter()

# Initialize the configs
web_scraper_config = WebScraperConfig.from_yaml(paths.WEB_SCRAPER_CONFIG_DIR)

''' API '''
@router.get('/scrape')
async def scrape(ticker: str) -> WebScraperResponse:
    '''
    Description: Scrapes yahoo finance for news articles

    Step 1: Search website and scrape using the ticker
    Step 1.1: Validate that it's a valid ticker by checking it found articles
    Step 2: Parse and extract article headlines

    Args:
        ticker (str): ticker of stock that we're scraping for
    
    Return:
        headline_list_response (WebScraperResponse): list of headlines
    '''

    try:
        async with httpx.AsyncClient(timeout=web_scraper_config.timeout) as client:

            # TODO: Add some validation that the ticker exists
            
            ''' Step 1: Fetch page '''
            # format URI
            ticker = ticker.upper()
            yahoo_finance_url = web_scraper_config.base_url.format(ticker=ticker)

            # Request page
            logger.info(f'Calling {yahoo_finance_url}')

            yahoo_articles_raw_data = await client.get(
                url=yahoo_finance_url, 
                headers=web_scraper_config.headers, 
                timeout=web_scraper_config.timeout
            )
            yahoo_articles_raw_data.raise_for_status()

            logger.info(f'Successfully retrieved articles from: {yahoo_finance_url}')

            ''' Step 2: Fetch headlines '''
            logger.info(f"Parsing raw data")

            soup = BeautifulSoup(yahoo_articles_raw_data.text, 'html.parser')
            headlines = soup.findAll('h3', class_='clamp yf-18q3fnf', limit=None)

            # Extract each string
            logger.info("Extracting headlines from soup")
            headline_list = [headline.text for headline in headlines]

            # Returning list of headlines
            headline_list_response = WebScraperResponse(headline_list=headline_list)
            return headline_list_response

    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=503,
            detail=f"Failed to fetch news: {str(e)}"
        )
    
