''' Headline Prediction code '''

from fastapi import APIRouter, HTTPException
from python_utils.logging.logging import init_logger
import asyncio
import yfinance as yf

from app.schemas.headline import HeadlineRequest, HeadlineConfig
from app.helpers.async_process import async_handler
from app.helpers.api import webscrape_headlines, ticker_price_history
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

    ''' Step 2: Scrape for articles and fetch ticker history '''

    headlines, ticker_hist = await asyncio.gather(
        webscrape_headlines(ticker=ticker, web_scraper_dns=headline_config.web_scraper_dns),
        ticker_price_history(ticker=ticker, ticker_info=ticker_info)
    )

    ''' Step 3: Run sentiment analysis '''
    headlines_sentiments = await async_handler(
        headlines=headlines,
        model_gateway=headline_config.model_gateway
    )

    return headlines_sentiments

    return {"message": "test"}