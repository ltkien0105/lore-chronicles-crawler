"""
Item pipelines for data transformation and Pydantic validation.
"""

from datetime import datetime

from pydantic import ValidationError

from src.models.champion_raw import (
    ChampionRaw,
    MetaData,
    Structure,
    Relation,
    KeyFacts,
    Titles,
    Characteristics,
    Age,
    PersonalStatus,
    ProfessionalStatus,
)
from src.scraper.markdown_converter import html_to_markdown


class MarkdownConversionPipeline:
    """
    Converts HTML content fields to markdown before validation.
    Priority: 200 (before PydanticValidationPipeline at 300)
    """

    # Fields to convert from HTML to markdown
    HTML_FIELDS = [
        "background",
        "appearance",
        "personality",
        "abilities",
        "trivia",
    ]

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        pipeline.spider = crawler.spider
        return pipeline

    def process_item(self, item: dict) -> dict:
        """Convert HTML fields to markdown."""

        # Convert content sections
        for field in self.HTML_FIELDS:
            if field in item and item[field]:
                original = item[field]
                item[field] = html_to_markdown(original)
                if item[field] != original and self.spider:
                    self.spider.logger.debug(f"Converted {field} to markdown")

        if self.spider:
            self.spider.logger.info(
                f"Converted HTML to markdown for: {item.get('name', 'unknown')}"
            )
        return item


class PydanticValidationPipeline:
    """
    Transforms flat ChampionItem into nested ChampionRaw structure
    and validates with Pydantic.
    """

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        pipeline.spider = crawler.spider
        return pipeline

    def process_item(self, item: dict) -> dict:
        """Process and validate item against ChampionRaw model."""
        try:
            # Build nested structure
            champion_raw = ChampionRaw(
                metadata=self._build_metadata(item),
                structure=self._build_structure(item),
                key_facts=self._build_key_facts(item),
            )

            if self.spider:
                self.spider.logger.info(
                    f"Validated champion: {champion_raw.structure.name}"
                )
            return champion_raw.model_dump(mode="json")

        except ValidationError as e:
            if self.spider:
                self.spider.logger.warning(
                    f"Validation failed for {item.get('source_url', 'unknown')}: "
                    f"{e.error_count()} errors"
                )
                # Log individual errors
                for error in e.errors():
                    self.spider.logger.debug(f"  - {error['loc']}: {error['msg']}")

            # Return partial data for debugging
            return {
                "source_url": item.get("source_url"),
                "name": item.get("name"),
                "validation_errors": [str(err) for err in e.errors()],
                "partial_data": dict(item),
            }

    def _build_metadata(self, item: dict) -> MetaData:
        """Build MetaData from item."""
        return MetaData(
            last_crawled=datetime.now(),
            source_url=item.get("source_url", ""),
        )

    def _build_structure(self, item: dict) -> Structure:
        """Build Structure from item."""
        # Parse relations list
        relations = []
        for rel in item.get("relations", []):
            if isinstance(rel, dict):
                relations.append(
                    Relation(
                        champion_name=rel.get("champion_name", ""),
                        source_url=rel.get("source_url", ""),
                        relationship_description=rel.get(
                            "relationship_description", ""
                        ),
                    )
                )

        return Structure(
            name=item.get("name", "Unknown"),
            quote=item.get("quote", "") or "",
            biography=item.get("biography", "") or "",
            background=item.get("background", "") or "",
            appearance=item.get("appearance", "") or "",
            personality=item.get("personality", "") or "",
            abilities=item.get("abilities", "") or "",
            relations=relations,
            relevant_links=item.get("relevant_links", []) or [],
            trivia=item.get("trivia", "") or "",
            role=item.get("role", "Unknown") or "Unknown",
            release_date=item.get("release_date", "Unknown") or "Unknown",
        )

    def _build_key_facts(self, item: dict) -> KeyFacts:
        """Build KeyFacts from item."""
        return KeyFacts(
            titles=Titles(
                real_name=item.get("real_name", "Unknown") or "Unknown",
                alias=item.get("alias", "Unknown") or "Unknown",
            ),
            characteristics=Characteristics(
                species=item.get("species", "Unknown") or "Unknown",
                pronoun=item.get("pronoun", []) or [],
                age=Age(
                    current=item.get("age_current", "Unknown") or "Unknown",
                    born_time=item.get("age_born_time", "Unknown") or "Unknown",
                ),
                weapons=item.get("weapons", "Unknown") or "Unknown",
            ),
            personal_status=PersonalStatus(
                status=item.get("status", "Unknown") or "Unknown",
                place_of_origin=item.get("place_of_origin", "Unknown") or "Unknown",
                current_residence=item.get("current_residence", "Unknown") or "Unknown",
                family=item.get("family", "Unknown") or "Unknown",
            ),
            professional_status=ProfessionalStatus(
                occupations=item.get("occupations", "Unknown") or "Unknown",
                regions=item.get("regions", "Unknown") or "Unknown",
                factions=item.get("factions", "Unknown") or "Unknown",
            ),
        )
