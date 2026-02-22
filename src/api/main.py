import requests
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from models.universe_meeps import UniverseMeeps
from models.faction import Faction

from utils.file_io import write_json_from_pydantic_model
from utils.riot_api import UniverseType, build_universe_url

response = requests.get(build_universe_url(UniverseType.SEARCH, language="en"))
# write_json_from_pydantic_model(
#     path="output/universe_meeps/overview.json", model=UniverseMeeps, response=result
# )
response = dict(response.json())
universer_meeps = UniverseMeeps.model_validate(response)
faction_slugs = [
    build_universe_url(UniverseType.FACTION, slug=faction.slug)
    for faction in universer_meeps.factions
]
for slug in faction_slugs:
    response = requests.get(slug)
    write_json_from_pydantic_model(
        path=f"output/universe_meeps/{slug.split('/')[-2]}_faction.json",
        model=Faction,
        response=response,
    )
