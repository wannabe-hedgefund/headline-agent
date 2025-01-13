''' Headline Prediction code '''

from fastapi import APIRouter, HTTPException
from python_utils.logging.logging import init_logger
import asyncio
import yfinance as yf
import httpx

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
    Step 4: Process sentiment analysis and historical data
    Step 5: Build a prompt
    Step 6: Send to LLM for price prediction.

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
        model_gateway=headline_config.slm_gateway
    )

    ''' Step 4: Process data '''
    
    # Get necessary ticker information
    logger.info(f"Processing historical price data of {ticker}")
    min_close = ticker_hist['Close'].min()
    min_close_date = ticker_hist['Close'].idxmin().strftime('%Y-%m-%d')
    max_close = ticker_hist['Close'].max()
    max_close_date = ticker_hist['Close'].idxmax().strftime('%Y-%m-%d')

    current_close = ticker_hist['Close'].iloc[-1]
    avg_close = ticker_hist['Close'].mean()

    # Reformat sentiment analysis for prompt
    logger.info(f'Re-formatting sentiment analysis for {ticker}')
    sentiment_summary = "Recent news analysis:\n"

    # Parse through list of sentiments and format it
    for i, sentiment in enumerate(headlines_sentiments, 1):
        '''
        Calculate dominant sentiment. 
        Aka the highest scoring sentiment for a headline.
        '''
        sentiments = {
            "Positive": sentiment.positive,
            "Neutral": sentiment.neutral,
            "Negative": sentiment.negative
        }
        '''
        Lambda notes:
        x: the tuple
        x[0]: Positive, Neutral, Negative
        x[1]: sentiment score

        So below method is comparing the sentiment scores to each other, finding the max value.
        We are returning the tuple, {Postive, 0.7} for example, as the max value.
        '''
        dominant_sentiment = max(sentiments.items(), key=lambda x: x[1])

        sentiment_summary += f"""\
            Article: {i}:
            Headline: {sentiment.headline}
            Dominate Sentiment: {dominant_sentiment[0]} ({dominant_sentiment[1]:.2f})
            Sentiment Distribution: {sentiment.positive:.2f} | Neu: {sentiment.neutral:.2f} | Neg: {sentiment.negative:.2f}
            """

    logger.info(f"Completed processing data for {ticker}. Building prompt.")

    ''' Step 5: Build prompt '''
    formatted_prompt = headline_config.llm_config.prompt_template.format(
        ticker=ticker,
        max_close=max_close,
        max_close_date=max_close_date,
        min_close=min_close,
        min_close_date=min_close_date,
        current_close=current_close,
        avg_close=avg_close,
        sentiment_summary=sentiment_summary
    )

    ''' Step 6: Send prompt to LLM '''
    logger.info(f"Sending request to LLM")

    llm_payload = {
        "model_name": headline_config.llm_config.llm_model,
        "prompt": formatted_prompt,
        "temperature": headline_config.llm_config.temperature
    }

    async with httpx.AsyncClient() as client:
        llm_response = await client.post(
            url=headline_config.llm_gateway,
            json=llm_payload
        )


    return llm_response