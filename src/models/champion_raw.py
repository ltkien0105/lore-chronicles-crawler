from datetime import datetime
from pydantic import BaseModel, Field


class MetaData(BaseModel):
    last_crawled: datetime = Field(
        default_factory=datetime.now,
        description="The timestamp when the data was last crawled.",
    )
    source_url: str = Field(
        ..., description="The URL from which the champion data was crawled."
    )


class Relation(BaseModel):
    champion_name: str = Field(..., description="The name of the related champion.")
    source_url: str = Field(..., description="The URL to the related champion's page.")
    relationship_description: str = Field(
        ...,
        description="A brief description of the relationship between the champions.",
    )


class Structure(BaseModel):
    name: str = Field(..., description="The name of the champion.")
    quote: str = Field(
        ..., description="A famous quote or tagline associated with the champion."
    )
    biography: str = Field(..., description="A biography link of the champion.")
    background: str = Field(
        ...,
        description="Background information about the champion. (save as markdown)",
    )
    appearance: str = Field(
        ...,
        description="Description of the champion's appearance. (save as markdown)",
    )
    personality: str = Field(
        ...,
        description="Description of the champion's personality. (save as markdown)",
    )
    abilities: str = Field(
        ...,
        description="A description of the champion's abilities. (save as markdown)",
    )
    relations: list[Relation] = Field(
        [],
        description="A list of relationships the champion has with other champions.",
    )
    relevant_links: list[str] = Field(
        [],
        description="A list of relevant links related to the champion.",
    )
    trivia: str = Field(
        ...,
        description="Trivia about the champion. (save as markdown)",
    )

    role: str = Field("Unknown", description="The role of the champion in the game.")
    release_date: str = Field(
        "Unknown", description="The date when the champion was released."
    )


class Titles(BaseModel):
    real_name: str = Field(..., description="The real name of the champion.")
    alias: list[str] = Field(
        [], description="A list of aliases or nicknames for the champion."
    )


class Age(BaseModel):
    current: str = Field("Unknown", description="The current age of the champion.")
    born_time: str = Field(
        "Unknown", description="The time when the champion was born."
    )


class PersonalStatus(BaseModel):
    status: str = Field(..., description="The status of the champion.")
    place_of_origin: str = Field(
        ..., description="The place of origin of the champion."
    )
    current_residence: str = Field(
        ..., description="The current residence of the champion."
    )
    family: str = Field(
        ..., description="Information about the champion's family. (save as markdown)"
    )


class ProfessionalStatus(BaseModel):
    occupations: str = Field(
        ..., description="The occupation of the champion. (save as markdown)"
    )
    regions: str = Field(
        ...,
        description="The affiliation or group the champion is associated with. (save as markdown)",
    )
    factions: str = Field(
        ..., description="The faction of the champion. (save as markdown)"
    )


class Characteristics(BaseModel):
    species: str = Field(..., description="The species of the champion.")
    pronoun: list[str] = Field(
        [], description="A list of pronouns associated with the champion."
    )
    age: Age = Field(..., description="The age details of the champion.")
    weapons: str = Field(
        ..., description="The weapon used by the champion. (save as markdown)"
    )


class KeyFacts(BaseModel):
    titles: Titles = Field(..., description="The titles of the champion.")
    characteristics: Characteristics = Field(
        ..., description="The characteristics of the champion."
    )
    personal_status: PersonalStatus = Field(
        ..., description="The personal status details of the champion."
    )
    professional_status: ProfessionalStatus = Field(
        ..., description="The professional status details of the champion."
    )


class ChampionRaw(BaseModel):
    metadata: MetaData = Field(..., description="Metadata about the champion data.")
    structure: Structure = Field(
        ..., description="The structural details of the champion."
    )
    key_facts: KeyFacts = Field(..., description="Key facts about the champion.")
