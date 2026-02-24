from pathlib import Path
import json

import requests

from models.faction import Faction
from models.universe_meeps import UniverseMeeps
from utils.file_io import write_json_from_pydantic_model
from utils.riot_api import UniverseType, build_universe_url


class RuneterraMapAPI:
    def __init__(self):
        pass

    @staticmethod
    def fetch_overview():
        response = requests.get(build_universe_url(UniverseType.SEARCH, language="en"))
        write_json_from_pydantic_model(
            path="output/universe_meeps/overview.json",
            model=UniverseMeeps,
            response=response,
        )

        return dict(response.json())

    @staticmethod
    def fetch_universe_meeps():
        result = None
        universe_meeps_path = Path("output/universe_meeps/overview.json")
        if not universe_meeps_path.exists():
            result = RuneterraMapAPI.fetch_overview()
        else:
            with open(universe_meeps_path, "r") as f:
                result = json.load(f)

        universer_meeps = UniverseMeeps.model_validate(result)
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
