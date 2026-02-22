from typing import List

from pydantic import BaseModel, Field
from .universe_meeps import Image


class Video(BaseModel):
    title: str
    subtitle: str
    description: str | List
    uri: str
    encoding: str | None = Field(None, alias="encoding")
    width: str | int | None = Field(None, alias="width")
    height: str | int | None = Field(None, alias="height")
    x: str | int | None = Field(None, alias="x")
    y: str | int | None = Field(None, alias="y")
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


class ExploreFaction(BaseModel):
    type: str
    title: str
    section_title: str = Field(..., alias="section-title")
    name: str
    slug: str
    description: str
    image: Image
    background: Image
    echelon: int | str = ""
    associated_champions: List[AssociatedChampion] = Field(
        ..., alias="associated-champions"
    )
    url: str


class FeaturedImage(Image):
    pass


class Module(BaseModel):
    slug: str
    type: str
    featured_image: FeaturedImage | str | None = Field(None, alias="featured-image")
    title: str
    subtitle: str | None = None
    description: str | None = None
    uri: str | None = None
    video: Video | None = None
    release_date: str | None = Field(None, alias="release-date")
    video_type: str | None = Field(None, alias="video-type")
    featured_champions: List | None = Field(None, alias="featured-champions")
    related_champions: List | None = Field(None, alias="related-champions")


class Faction(BaseModel):
    id: str
    name: str
    locale: str
    faction: ChildFaction
    champion_list_order: int = Field(..., alias="champion-list-order")
    associated_champions: List[AssociatedChampion] = Field(
        ..., alias="associated-champions"
    )
    explore_factions: List[ExploreFaction] = Field(..., alias="explore-factions")
    modules: List[Module]
