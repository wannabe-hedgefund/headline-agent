''' Headline Prediction code '''

from fastapi import APIRouter
from python_utils.logging.logging import init_logger

from app.schemas.headline import HeadlineRequest

# Initialize logger
logger = init_logger()

# Initialize the router
router = APIRouter()

''' API '''
@router.post('/predict')
async def predict(headline_request: HeadlineRequest):
    '''
    Description: Predict specific stock trend using sentiment analysis

    Step 1.1: Web-scrape news articles using ticker
    Step 1.2: Fetch historical stock price data via yfinance
    Step 2: Run sentiment analysis on news article's headlines (maybe entire article)
    Step 3: Gather sentiment over all recent news articles and historcal price and build a prompt
    Step 4: Send to LLM for price prediction.

    Args:
        headline_request: user input of ticker they want to check

    Return:
        TBD
    '''
    pass