''' Schemas for headline '''

from pydantic import BaseModel
import yaml

class HeadlineRequest(BaseModel):
    stock_ticker: str

class LLMConfig(BaseModel):
    llm_model: str
    temperature: float
    prompt_template: str

class HeadlineConfig(BaseModel):
    web_scraper_dns: str
    slm_gateway: str
    llm_gateway: str
    sentiment_model: str
    llm_config: LLMConfig

    @classmethod
    def from_yaml(cls, file: str) -> 'HeadlineConfig':
        with open(file, "r") as f:
            config_dict = yaml.safe_load(f)
        return cls.model_validate(config_dict)

class RobertaSentimentResponse(BaseModel):
    headline: str
    negative: float
    neutral: float
    positive: float