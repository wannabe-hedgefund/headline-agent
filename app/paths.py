import os
from pathlib import Path

_ROOT_DIR = Path(os.path.abspath(__file__)).parent

# Web Scraper config
WEB_SCRAPER_CONFIG_DIR = _ROOT_DIR / "configs/web_scraper.yaml"
WEB_SCRAPER_SERVICE_CONFIG_PATH = Path(os.environ.get("SERVICE_CONFIG_PATH", str(WEB_SCRAPER_CONFIG_DIR)))

# Headline Service config
SERVICE_CONFIG_DIR = _ROOT_DIR / "configs/config.yaml"
SERVICE_CONFIG_PATH = Path(os.environ.get("SERVICE_CONFIG_PATH", str(SERVICE_CONFIG_DIR)))