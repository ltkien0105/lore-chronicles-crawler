from typing import List

from pydantic import BaseModel, Field
from .universe_meeps import Image


class Video(BaseModel):
    title: str
    subtitle: str
    description: str
    uri: str
    encoding: str
    width: int | None = None
    height: int | None = None
    x: int | None = None
    y: int | None = None
    featured_champions: List = Field(..., alias="featured-champions")


class Overview(BaseModel):
    short: str


class Race(BaseModel):
    name: str
    slug: str


class Role(BaseModel):
    name: str
    slug: str


class Biography(BaseModel):
    full: str
    short: str
    quote: str
    quote_author: str = Field(..., alias="quote-author")


class AssociatedChampion(BaseModel):
    type: str
    release_date: str = Field(..., alias="release-date")
    name: str
    title: str
    section_title: str = Field(..., alias="section-title")
    slug: str
    associated_faction: str = Field(..., alias="associated-faction")
    associated_faction_slug: str = Field(..., alias="associated-faction-slug")
    image: Image
    background: Image
    url: str
    video: Video | None = None
    races: List[Race]
    roles: List[Role]
    role: List[Role]
    game_info_url: str | None = Field(None, alias="game-info-url")
    biography: Biography
    header_image: str | None = Field(None, alias="headerImage")
    subtitle: str
    echelon: int


class ChildFaction(BaseModel):
    slug: str
    image: Image
    video: Video
    name: str
    overview: Overview
    header_image: str = Field(..., alias="headerImage")


class Faction(BaseModel):
    id: str
    name: str
    locale: str
    faction: ChildFaction
    champion_list_order: int = Field(..., alias="champion-list-order")
    associated_champions: List[AssociatedChampion] = Field(
        ..., alias="associated-champions"
    )
