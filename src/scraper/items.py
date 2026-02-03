"""
Minimal Scrapy Item definitions.
Primary validation done via Pydantic in pipelines.py
"""
import scrapy


class ChampionItem(scrapy.Item):
    """Raw champion data extracted from wiki page."""

    # Metadata
    source_url = scrapy.Field()

    # Structure fields
    name = scrapy.Field()
    quote = scrapy.Field()
    biography = scrapy.Field()
    background = scrapy.Field()
    appearance = scrapy.Field()
    personality = scrapy.Field()
    abilities = scrapy.Field()
    relations = scrapy.Field()
    relevant_links = scrapy.Field()
    trivia = scrapy.Field()
    role = scrapy.Field()
    release_date = scrapy.Field()

    # Key facts - Titles
    real_name = scrapy.Field()
    alias = scrapy.Field()

    # Key facts - Characteristics
    species = scrapy.Field()
    pronoun = scrapy.Field()
    age_current = scrapy.Field()
    age_born_time = scrapy.Field()
    weapons = scrapy.Field()

    # Key facts - Personal status
    status = scrapy.Field()
    place_of_origin = scrapy.Field()
    current_residence = scrapy.Field()
    family = scrapy.Field()

    # Key facts - Professional status
    occupations = scrapy.Field()
    regions = scrapy.Field()
    factions = scrapy.Field()
