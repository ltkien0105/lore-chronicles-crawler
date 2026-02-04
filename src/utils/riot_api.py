import requests


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
