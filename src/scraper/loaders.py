"""
ItemLoader definitions with field processors.
"""
import re
from itemloaders.processors import MapCompose, TakeFirst, Join, Identity
from scrapy.loader import ItemLoader

from src.scraper.items import ChampionItem


def strip_text(value: str) -> str:
    """Strip whitespace from text values."""
    if isinstance(value, str):
        return value.strip()
    return value


def clean_whitespace(value: str) -> str:
    """Normalize multiple whitespace to single space."""
    if isinstance(value, str):
        return " ".join(value.split())
    return value


def remove_edit_markers(value: str) -> str:
    """Remove [edit] markers from wiki content."""
    if isinstance(value, str):
        value = re.sub(r'\[edit\]', '', value, flags=re.IGNORECASE)
        value = re.sub(r'\[Edit\]', '', value)
        return value
    return value


class ChampionLoader(ItemLoader):
    """ItemLoader for champion data with default processors."""

    default_item_class = ChampionItem

    # Default: take first value, strip whitespace
    default_input_processor = MapCompose(strip_text, clean_whitespace)
    default_output_processor = TakeFirst()

    # List fields - keep as lists
    alias_out = Identity()
    pronoun_out = Identity()
    relations_out = Identity()
    relevant_links_out = Identity()
    abilities_out = Identity()

    # HTML content - join multiple elements
    background_out = Join("\n")
    appearance_out = Join("\n")
    personality_out = Join("\n")
    trivia_out = Join("\n")

    # Clean wiki artifacts from content
    background_in = MapCompose(strip_text, remove_edit_markers)
    appearance_in = MapCompose(strip_text, remove_edit_markers)
    personality_in = MapCompose(strip_text, remove_edit_markers)
    trivia_in = MapCompose(strip_text, remove_edit_markers)
