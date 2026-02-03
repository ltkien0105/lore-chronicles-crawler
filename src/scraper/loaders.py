"""
ItemLoader definitions with field processors.
Full implementation in Phase 03.
"""
from itemloaders.processors import MapCompose, TakeFirst, Identity
from scrapy.loader import ItemLoader

from src.scraper.items import ChampionItem


def strip_text(value: str) -> str:
    """Strip whitespace from text values."""
    if isinstance(value, str):
        return value.strip()
    return value


class ChampionLoader(ItemLoader):
    """ItemLoader for champion data with default processors."""

    default_item_class = ChampionItem

    # Default: take first value, strip whitespace
    default_input_processor = MapCompose(strip_text)
    default_output_processor = TakeFirst()

    # List fields - keep as lists
    alias_out = Identity()
    pronoun_out = Identity()
    relations_out = Identity()
    relevant_links_out = Identity()
    abilities_out = Identity()
