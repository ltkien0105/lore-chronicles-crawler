import requests
import sys
from pathlib import Path

from api_config import BASE_URL, LANGUAGES

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from models.universe_meeps import UniverseMeeps
from utils.file_io import write_json_from_pydantic_model

response = requests.get(f"{BASE_URL}/{LANGUAGES['en']}/search/index.json")
write_json_from_pydantic_model(
    path="output/universe_meeps/overview.json", model=UniverseMeeps, response=response
)
