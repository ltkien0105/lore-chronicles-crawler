import requests
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from api.runeterra_map_api import RuneterraMapAPI

RuneterraMapAPI.fetch_universe_meeps()

# URL = "https://map.leagueoflegends.com/loc/content-panels-en_us.json"
# URL = "https://map.leagueoflegends.com/loc/content-panel-cards-en_us.json"
# filename = URL.split("/")[-1]
# response = requests.get(URL)
# write_json_from_pydantic_model(
#     path=f"output/{filename}",
#     model=ContentPanelCard,
#     response=response,
# )
