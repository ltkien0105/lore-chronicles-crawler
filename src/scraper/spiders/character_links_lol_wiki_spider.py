import scrapy
from urllib.parse import urljoin

from src.utils.constants import BASE_URL_WIKI


class CharacterLinksLolWikiSpider(scrapy.Spider):
    name = "character_links_lol_wiki"
    allowed_domains = ["wiki.leagueoflegends.com"]
    start_urls = ["https://wiki.leagueoflegends.com/en-us/Category:Characters"]
    custom_settings = {
        # Output settings - single champion_links.json file
        "FEED_EXPORT_ENCODING": "utf-8",
        "FEEDS": {
            "output/champion_links.json": {
                "format": "json",
                "encoding": "utf8",
                "indent": 2,
                "overwrite": True,
            }
        },
    }

    def parse(self, response):
        character_cells = response.xpath("//table//tr")
        character_links = {}

        for cell in character_cells:
            title = cell.xpath("./th/a/text()").get()
            if title not in character_links:
                character_links[title] = []

            links = sorted(
                set(
                    cell.xpath(
                        "./td//a[contains(@title, 'Universe:')][contains(@href, 'Universe:')]/@href"
                    ).getall()
                )
            )

            full_links = [urljoin(BASE_URL_WIKI, link) for link in links]
            character_links[title].extend(full_links)

        yield character_links
