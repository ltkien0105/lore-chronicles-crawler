"""
LOL Wiki Universe Spider - Extracts champion lore data.
"""

import scrapy
from scrapy.http import Response
from urllib.parse import urljoin, unquote

from src.scraper.markdown_converter import clean_markdown, html_to_markdown
from src.scraper.items import ChampionItem
from src.utils.constants import BASE_URL_WIKI, UNIVERSE_WIKI


class LolWikiSpider(scrapy.Spider):
    """Spider for crawling League of Legends Wiki Universe pages."""

    name = "lol_wiki"
    allowed_domains = ["wiki.leagueoflegends.com"]

    # Default champions to crawl
    champion_names = ["Cho'Gath", "Kai'Sa", "Darius"]

    def __init__(self, champion_names=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if champion_names:
            self.champion_names = [c.strip() for c in champion_names.split(",")]

    async def start(self):
        """Generate initial requests for champion pages."""
        for champion in self.champion_names:
            url = f"{UNIVERSE_WIKI}{champion}"
            yield scrapy.Request(
                url, callback=self.parse, cb_kwargs={"champion_name": champion}
            )

    def parse(self, response, champion_name: str = None):
        """Parse champion Universe page and extract all data."""
        item = ChampionItem()

        # Metadata
        item["source_url"] = response.url

        # === Structure Fields ===
        item["name"] = self._extract_name(response)
        item["quote"] = self._extract_quote(response)
        item["biography"] = self._extract_biography_link(response)

        # Content sections (raw HTML - converted to markdown in pipeline)
        item["background"] = self._extract_section_html(response, "Background")
        item["appearance"] = self._extract_section_html(response, "Appearance")
        item["personality"] = self._extract_section_html(response, "Personality")
        item["abilities"] = self._extract_section_html(response, "Abilities")
        item["trivia"] = self._extract_section_html(response, "Trivia")

        # Relations and links
        item["relations"] = self._extract_relations(response)
        item["relevant_links"] = self._extract_relevant_links(response)

        # Role and release date (may not be on Universe page)
        item["role"] = self._extract_infobox_field(response, "Role") or "Unknown"
        item["release_date"] = (
            self._extract_infobox_field(response, "Release") or "Unknown"
        )

        # === Key Facts - Titles ===
        item["real_name"] = (
            self._extract_infobox_field(response, "Real Name") or "Unknown"
        )
        item["alias"] = self._extract_infobox_list(response, "Alias")

        # === Key Facts - Characteristics ===
        item["species"] = self._extract_infobox_field(response, "Species") or "Unknown"
        item["pronoun"] = self._extract_infobox_list(response, "Pronoun")
        item["age_current"] = self._extract_infobox_field(response, "Age") or "Unknown"
        item["age_born_time"] = (
            self._extract_infobox_field(response, "Born") or "Unknown"
        )
        item["weapons"] = self._extract_infobox_field(response, "Weapon") or "Unknown"

        # === Key Facts - Personal Status ===
        item["status"] = self._extract_infobox_field(response, "Status") or "Unknown"
        item["place_of_origin"] = (
            self._extract_infobox_field(response, "Origin") or "Unknown"
        )
        item["current_residence"] = (
            self._extract_infobox_field(response, "Residence") or "Unknown"
        )
        item["family"] = self._extract_infobox_field(response, "Family") or "Unknown"

        # === Key Facts - Professional Status ===
        item["occupations"] = (
            self._extract_infobox_field(response, "Occupation") or "Unknown"
        )
        item["regions"] = self._extract_infobox_field(response, "Region") or "Unknown"
        item["factions"] = self._extract_infobox_field(response, "Faction") or "Unknown"

        yield item

    # === Helper Methods ===

    def _extract_name(self, response) -> str:
        """Extract champion name from page title."""
        name = response.xpath(
            '//h1[contains(@class, "mw-page-title-main")]/text()'
        ).get()
        if not name:
            # Fallback: extract from URL
            name = unquote(response.url.split(":")[-1])
        return name.strip() if name else ""

    def _extract_quote(self, response) -> str:
        """Extract champion quote from blockquote or infobox."""
        quote = response.xpath('//table[contains(@class, "background-quote")]//i').get()

        return clean_markdown(html_to_markdown(quote)) if quote else ""

    def _extract_biography_link(self, response) -> str:
        """Extract link to full biography page."""
        bio_link = response.xpath('//a[contains(text(), "Read Biography")]/@href').get()
        if bio_link:
            return urljoin(BASE_URL_WIKI, bio_link)
        return ""

    def _extract_section_html(self, response, section_id: str) -> str:
        """Extract HTML content between h2 section and next h2."""
        # Find all content after the div contains mw-heading2 until next div contains mw-heading2

        section_order = {
            "Background": 1,
            "Appearance": 2,
            "Personality": 3,
            "Abilities": 4,
            "Relations": 5,
            "Read More": 6,
            "Trivia": 7,
        }

        paragraphs = response.xpath(
            "//div[contains(@class, 'mw-heading2')]/following-sibling::*"
            "[self::p or self::div or h3 or self::ul or self::ol or self::dl][preceding-sibling::div[contains(@class, 'mw-heading2')]]"
            f"[count(preceding-sibling::div[contains(@class, 'mw-heading2')]) = {section_order[section_id]}]"
        ).getall()

        if not paragraphs:
            # Alternative: simpler selector
            paragraphs = response.xpath(
                f'//h2[@id="{section_id}"]/following-sibling::p'
            ).getall()

        return "\n".join(paragraphs) if paragraphs else ""

    def _extract_relations(self, response: Response) -> list:
        """Extract champion relations from Relations/Related characters section only."""
        relations = []
        seen = {}

        # Only look in the Relations section for actual champion relationships
        # Find the Relations h2/h3 section and extract Universe links from there
        relations_section = response.xpath(
            "//div[contains(@class, 'mw-heading2')]/following-sibling::*"
            "[self::p or self::div or h3 or self::ul or self::ol or self::dl][preceding-sibling::div[contains(@class, 'mw-heading2')]]"
            "[count(preceding-sibling::div[contains(@class, 'mw-heading2')]) = 5]"
        )

        nearest_relation_char = None
        for section in relations_section:
            if section.css("::text").get() is None:
                continue

            section_class = section.xpath("@class").get() or ""
            if "mw-heading2" in section_class:
                continue

            if "mw-heading3" in section_class:
                # Extract relation character name
                relation_char_name = section.xpath("./h3[1]/@id").get()
                href = (
                    section.xpath('.//a[contains(@href, "/Universe:")]')
                    .xpath("@href")
                    .get()
                )
                nearest_relation_char = relation_char_name
                # Skip if already seen
                if relation_char_name in seen:
                    return
                seen[relation_char_name] = {
                    "source_url": urljoin(BASE_URL_WIKI, href),
                    "relationship_description": "",
                }
            else:
                if nearest_relation_char is None:
                    continue
                seen[nearest_relation_char]["relationship_description"] += (
                    f"\n{section.get()}"
                )

        for champ_name, relation_info in seen.items():
            relations.append(
                {
                    "champion_name": champ_name,
                    "source_url": relation_info["source_url"],
                    "relationship_description": html_to_markdown(
                        relation_info["relationship_description"]
                    ),
                }
            )

        return relations

    def _extract_relevant_links(self, response) -> list:
        """Extract all relevant Universe and story links (excluding edit links)."""
        links = []
        for href in response.xpath('//a[contains(@href, "/Universe:")]/@href').getall():
            # Skip edit links
            if "action=edit" in href or "veaction=edit" in href:
                continue
            full_url = urljoin(BASE_URL_WIKI, href)
            if full_url not in links and full_url != response.url:
                links.append(full_url)
        return links

    def _extract_infobox_field(self, response, label: str) -> str:
        """Extract single value from infobox table row."""
        # Try multiple patterns for MediaWiki infobox structure

        # Pattern 1: th/td with direct text match
        value = response.xpath(
            f'//th[contains(text(), "{label}")]/following-sibling::td//text()'
        ).getall()
        if value:
            return " ".join(v.strip() for v in value if v.strip())

        # Pattern 2: th with nested element containing text
        value = response.xpath(
            f'//th[.//text()[contains(., "{label}")]]/following-sibling::td//text()'
        ).getall()
        if value:
            return " ".join(v.strip() for v in value if v.strip())

        # Pattern 3: td/td pattern (some infoboxes use this)
        value = response.xpath(
            f'//td[contains(text(), "{label}")]/following-sibling::td//text()'
        ).getall()
        if value:
            return " ".join(v.strip() for v in value if v.strip())

        # Pattern 4: div-based infobox (newer wikis)
        value = response.xpath(
            f'//*[contains(@class, "infobox")]//*[contains(text(), "{label}")]/following-sibling::*//text()'
        ).getall()
        if value:
            return " ".join(v.strip() for v in value if v.strip())

        return ""

    def _extract_infobox_list(self, response, label: str) -> list:
        """Extract list values from infobox (e.g., aliases, pronouns)."""
        # Get all text from the cell using multiple patterns
        values = response.xpath(
            f'//th[contains(text(), "{label}")]/following-sibling::td//text()'
        ).getall()

        if not values:
            values = response.xpath(
                f'//th[.//text()[contains(., "{label}")]]/following-sibling::td//text()'
            ).getall()

        if not values:
            values = response.xpath(
                f'//td[contains(text(), "{label}")]/following-sibling::td//text()'
            ).getall()

        if not values:
            values = response.xpath(
                f'//*[contains(@class, "infobox")]//*[contains(text(), "{label}")]/following-sibling::*//text()'
            ).getall()

        # Clean and split by common separators
        cleaned = []
        for v in values:
            v = v.strip()
            if v and v not in [",", "/", "|", "•"]:
                cleaned.append(v)

        return cleaned
