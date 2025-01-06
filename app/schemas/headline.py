''' Schemas for headline '''

from pydantic import BaseModel

class HeadlineRequest(BaseModel):
    stock_ticker: str