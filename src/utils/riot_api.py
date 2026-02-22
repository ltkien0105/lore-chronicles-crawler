import requests
from api.api_config import BASE_URL, LANGUAGES


def get_latest_version() -> str:
    response = requests.get("https://ddragon.leagueoflegends.com/api/versions.json")

    return response.json()[0]


def get_champion_names() -> list[str]:
    version = get_latest_version()
    response = requests.get(
        f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion.json"
    )
    data = response.json()
    return [champion["name"] for champion in data["data"].values()]


class UniverseType:
    SEARCH = "search/index.json"
    FACTION_BROWSE = "faction-browse/index.json"
    FACTION = "factions/{slug}/index.json"


def build_universe_url(
    universe_type: UniverseType, language: str = "en", **kwargs
) -> str:
    if universe_type == UniverseType.SEARCH:
        return f"{BASE_URL}/{LANGUAGES[language]}/{UniverseType.SEARCH}"
    elif universe_type == UniverseType.FACTION_BROWSE:
        return f"{BASE_URL}/{LANGUAGES[language]}/{UniverseType.FACTION_BROWSE}"
    elif universe_type == UniverseType.FACTION:
        slug = kwargs.get("slug")
        if not slug:
            raise ValueError("Slug is required for FACTION universe type")
        return (
            f"{BASE_URL}/{LANGUAGES[language]}/{UniverseType.FACTION.format(slug=slug)}"
        )
    else:
        raise ValueError("Invalid universe type")
