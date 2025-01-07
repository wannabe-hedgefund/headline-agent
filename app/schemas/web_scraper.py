''' Schemas for the web-scraper '''

import yaml
from pydantic import BaseModel

class WebScraperConfig(BaseModel):
    base_url: str
    timeout: int

    @classmethod
    def from_yaml(cls, file: str) -> 'WebScraperConfig':
        with open(file, "r") as f:
            config_dict = yaml.safe_load(f)
        return cls.model_validate(config_dict)
    
