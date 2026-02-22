from typing import List

from pydantic import BaseModel, Field


class Image(BaseModel):
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


class Background(BaseModel):
    title: str
    subtitle: str
    description: str
    uri: str
    encoding: str
    width: int
    height: int
    x: int
    y: int
    featured_champions: List = Field(..., alias="featured-champions")


class Champion(BaseModel):
    type: str
    release_date: str = Field(..., alias="release-date")
    name: str
    title: str
    section_title: str = Field(..., alias="section-title")
    slug: str
    associated_faction: str = Field(..., alias="associated-faction")
    associated_faction_slug: str = Field(..., alias="associated-faction-slug")
    image: Image
    background: Background
    url: str


class Faction(BaseModel):
    type: str
    title: str
    section_title: str = Field(..., alias="section-title")
    name: str
    slug: str
    description: str
    image: Image
    background: Background
    echelon: str
    associated_champions: List = Field(..., alias="associated-champions")
    url: str


class UniverseMeeps(BaseModel):
    id: str
    name: str
    locale: str
    champions: List[Champion]
    factions: List[Faction]
