''' Web scraper code '''

from fastapi import APIRouter
from python_utils.logging.logging import init_logger
from bs4 import BeautifulSoup

from app.schemas.web_scraper import WebScraperConfig
from app import paths

# Initialize logger
logger = init_logger()

# Initialize the router
router = APIRouter()

# Initialize the configs
config = WebScraperConfig.from_yaml(paths.WEB_SCRAPER_CONFIG_DIR)

''' API '''
@router.post('/web-scrape')
async def scrape(ticker: str):
    '''
    Description: Scrapes yahoo finance for news articles

    Args:
        ticker (str): ticker of stock that we're scraping for
    
    Return:
        TBD
    '''
    

