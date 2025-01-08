''' Headline Prediction code '''

from fastapi import APIRouter, HTTPException
from python_utils.logging.logging import init_logger
from datetime import datetime, timedelta
import yfinance as yf
import httpx

from app.schemas.headline import HeadlineRequest, HeadlineConfig
from app import paths

# Initialize logger
logger = init_logger()

# Load configurations
headline_config = HeadlineConfig.from_yaml(paths.SERVICE_CONFIG_PATH)

# Initialize the router
router = APIRouter()

''' API '''
@router.post('/predict')
async def predict(headline_request: HeadlineRequest):
    '''
    Description: Predict specific stock trend using sentiment analysis

    Step 1: Validate ticker
    Step 2.1: Web-scrape news articles using ticker
    Step 2.2: Fetch historical stock price data via yfinance
    Step 3: Run sentiment analysis on news article's headlines (maybe entire article)
    Step 4: Gather sentiment over all recent news articles and historcal price and build a prompt
    Step 5: Send to LLM for price prediction.

    Args:
        headline_request: user input of ticker they want to check

    Return:
        TBD
    '''
    
    ''' Step 1: Validate ticker '''

    ticker = headline_request.stock_ticker

    logger.info(f"Validing if {ticker} is valid.")

    ticker_info = yf.Ticker(ticker.upper()) # This will be re-used later
    info = ticker_info.info
    if info['trailingPegRatio'] is None:
        raise HTTPException(status_code=400, detail='Invalid ticker')
    
    logger.info(f"{ticker} is valid.")

    # TODO: use Thread library for multi-threading. Need to disable GIL. Combine step 2.1 and 2.2
    ''' Step 2.1: Scrape for articles '''

    logger.info(f"Looking for headlines for {ticker}")
    web_scraper_url = headline_config.web_scraper_dns
    params = {
        "ticker": ticker
    }

    async with httpx.AsyncClient() as client:
        web_scraper_response = await client.get(
            url=web_scraper_url,
            params=params
        )

    headlines = web_scraper_response.json()["headline_list"]

    ''' Step 2.2: Historical stock data '''
    logger.info(f'Fetching 1mo of {ticker} price data')
    
    stock_data_end_date = datetime.now()
    stock_data_start_date = stock_data_end_date - timedelta(days=31)
    ticker_hist = ticker_info.history(start=stock_data_start_date)
    logger.info(f'Successfully fetched price history of {ticker}')

    return {"message": "test"}