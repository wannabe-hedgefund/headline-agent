''' External 3rd party APIs '''

from python_utils.logging.logging import init_logger
from yfinance import Ticker
from pandas import DataFrame
from datetime import datetime, timedelta
import httpx

from typing import List

# Initialize logger
logger = init_logger()

async def webscrape_headlines(ticker: str, web_scraper_dns: str) -> List[str]:
    '''
    Description: takes in ticker and scrapes yahoo finance

    Args:
        ticker: ticker of stock
        web_scraper_dns: yahoo finance link to articles

    Returns:
        web_scraper_response: returns list of headlines
    '''
    logger.info(f"Looking for headlines for {ticker}")
    web_scraper_url = web_scraper_dns
    params = {
        "ticker": ticker
    }

    async with httpx.AsyncClient() as client:
        logger.info(f"Calling {web_scraper_url}")
        web_scraper_response = await client.get(
            url=web_scraper_url,
            params=params
        )

    # Fetched list of headlines of ticker
    logger.info(f"Successfully fetched latest news articles for {ticker}")
    
    return web_scraper_response.json()["headline_list"]

async def ticker_price_history(ticker: str, ticker_info: Ticker) -> DataFrame:
    '''
    Description: Fetches the ticker price history

    Args:
        ticker: The ticker of stock. Used only for logging
        ticker_info: ticker info from yf

    Returns:
        ticker_hist (DataFrame): DataFrame of ticker price history
    '''
    logger.info(f'Fetching 1mo of {ticker} price data')
    
    stock_data_end_date = datetime.now()
    stock_data_start_date = stock_data_end_date - timedelta(days=31)
    ticker_hist = ticker_info.history(start=stock_data_start_date)

    logger.info(f"Successfully fetched 1mo of {ticker} price data")

    return ticker_hist