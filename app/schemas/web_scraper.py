''' Schemas for the web-scraper '''

import yaml
from pydantic import BaseModel
from typing import Dict, List

class WebScraperConfig(BaseModel):
    base_url: str
    headers: Dict[str, str]
    timeout: int
    min_articles: int
    max_articles: int

    @classmethod
    def from_yaml(cls, file: str) -> 'WebScraperConfig':
        with open(file, "r") as f:
            config_dict = yaml.safe_load(f)
        return cls.model_validate(config_dict)
    
class WebScraperResponse(BaseModel):
    headline_list: List[str]