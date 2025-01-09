''' Purpose of this file is to have a way to send a list of headlines concurently to sentiment model. '''

import asyncio
import httpx
from typing import List
from python_utils.logging.logging import init_logger

from app.schemas.headline import RobertaSentimentResponse

# Initialize logger
logger = init_logger()

async def headline_sentiment(
        client: httpx.AsyncClient, 
        headline: str, 
        model_gateway: str
    ) -> RobertaSentimentResponse:
    '''
    Description: forwards request to sentiment model

    Args:
        client: httpx async client
        headline: the headline sent for sentiment analysis
        model_gateway: url of sentiment model

    Return:
        headline_sentiment_response: sentiment analysis from roberta model
    '''
    payload = {
        "model_name": "roberta_sentiment",
        "prompt": headline
    }

    logger.info(f"Sending {headline} to {model_gateway}")

    response = await client.post(
        url=model_gateway,
        json=payload
    )
    response = response.json()

    logger.info(f"Retrived sentiment for {headline}")

    return RobertaSentimentResponse(
        headline=headline,
        negative=response["negative"],
        neutral=response["neutral"],
        positive=response["positive"]
    )

async def async_handler(headlines: List[str], model_gateway: str) -> List[RobertaSentimentResponse]:
    '''
    Description: This will send requests in parallel to the roberta model

    Args:
        headlines (List[str]): list of headlines to process their sentiment.

    Return:
        headlines_sentiments (List[RobertaSentimentResponse]): List of sentiment
    '''

    async with httpx.AsyncClient() as client:
        # list of functions to call sentiment
        tasks = [
            headline_sentiment(client=client, headline=headline, model_gateway=model_gateway) for headline in headlines
        ]

        # Asyncio will call all functions in tasks concurrently
        logger.info("Processing headlines concurrently")
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Filter out any failed requests and log them
        headlines_sentiments = []
        for result in results:
            if isinstance(result, Exception):
                logger.info(f"Error processing headline: {str(result)}")
            else:
                headlines_sentiments.append(result)
                
        return headlines_sentiments
