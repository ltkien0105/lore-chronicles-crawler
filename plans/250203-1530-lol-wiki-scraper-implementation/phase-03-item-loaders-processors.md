# Phase 03: Item Loaders & Processors

## Context Links

- [Main Plan](./plan.md)
- [Phase 02: Spider](./phase-02-spider-implementation.md)
- [Scrapy Patterns Research](./research/researcher-02-scrapy-patterns.md)
- [ChampionRaw Model](../src/models/champion_raw.py)

---

## Overview

| Field | Value |
|-------|-------|
| Priority | High |
| Status | pending |
| Description | Implement ItemLoader with field processors and Pydantic validation pipeline |

---

## Key Insights

### From Scrapy Patterns Research

1. **ItemLoader + Pydantic** - Best practice: ItemLoader for extraction, Pydantic for validation
2. **MapCompose** - Apply multiple processors in sequence to each value
3. **TakeFirst** - Output processor to get single value from list
4. **Join** - Output processor to concatenate list values

### Processing Pipeline

```
Spider yields ChampionItem
    ↓
ItemLoader (optional preprocessing)
    ↓
PydanticValidationPipeline
    ├─→ Transform flat item → nested ChampionRaw structure
    ├─→ Validate with Pydantic
    └─→ Yield validated dict (for JSON output)
```

---

## Requirements

### Functional
- Clean extracted text (strip whitespace, normalize)
- Transform flat ChampionItem → nested ChampionRaw structure
- Validate all required fields present
- Log validation errors without crashing
- Output clean JSON matching ChampionRaw schema

### Non-Functional
- Graceful handling of missing optional fields
- Partial data saved on validation failure
- Clear error messages for debugging

---

## Architecture

### Data Flow

```
ChampionItem (flat structure)
    │
    ▼
┌─────────────────────────────┐
│ PydanticValidationPipeline  │
│  ├─ _build_metadata()       │
│  ├─ _build_structure()      │
│  ├─ _build_key_facts()      │
│  └─ ChampionRaw.model_validate()
└─────────────────────────────┘
    │
    ▼
Validated dict → JSON output
```

### Field Mapping

| ChampionItem Field | ChampionRaw Path |
|-------------------|------------------|
| source_url | metadata.source_url |
| name | structure.name |
| quote | structure.quote |
| biography | structure.biography |
| background | structure.background |
| appearance | structure.appearance |
| personality | structure.personality |
| abilities | structure.abilities |
| relations | structure.relations[] |
| relevant_links | structure.relevant_links[] |
| trivia | structure.trivia |
| role | structure.role |
| release_date | structure.release_date |
| real_name | key_facts.titles.real_name |
| alias | key_facts.titles.alias[] |
| species | key_facts.characteristics.species |
| pronoun | key_facts.characteristics.pronoun[] |
| age_current | key_facts.characteristics.age.current |
| age_born_time | key_facts.characteristics.age.born_time |
| weapons | key_facts.characteristics.weapons |
| status | key_facts.personal_status.status |
| place_of_origin | key_facts.personal_status.place_of_origin |
| current_residence | key_facts.personal_status.current_residence |
| family | key_facts.personal_status.family |
| occupations | key_facts.professional_status.occupations |
| regions | key_facts.professional_status.regions |
| factions | key_facts.professional_status.factions |

---

## Related Code Files

### Files to Modify
- `src/scraper/pipelines.py` - Full implementation
- `src/scraper/loaders.py` - ItemLoader definitions
- `src/scraper/settings.py` - Enable pipeline

### Files to Reference
- `src/scraper/items.py` - ChampionItem structure
- `src/models/champion_raw.py` - Target Pydantic model

---

## Implementation Steps

### Step 1: Create loaders.py

```python
"""
ItemLoader definitions with field processors.
"""
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
        return value.replace("[edit]", "").replace("[Edit]", "")
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

    # HTML content - join multiple elements
    background_out = Join("\n")
    appearance_out = Join("\n")
    personality_out = Join("\n")
    abilities_out = Join("\n")
    trivia_out = Join("\n")

    # Clean wiki artifacts from content
    background_in = MapCompose(strip_text, remove_edit_markers)
    appearance_in = MapCompose(strip_text, remove_edit_markers)
    personality_in = MapCompose(strip_text, remove_edit_markers)
    trivia_in = MapCompose(strip_text, remove_edit_markers)
```

### Step 2: Implement pipelines.py

```python
"""
Item pipelines for data transformation and Pydantic validation.
"""
from datetime import datetime
from typing import Any

from pydantic import ValidationError
from scrapy.exceptions import DropItem

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


class PydanticValidationPipeline:
    """
    Transforms flat ChampionItem into nested ChampionRaw structure
    and validates with Pydantic.
    """

    def process_item(self, item: dict, spider) -> dict:
        """Process and validate item against ChampionRaw model."""
        try:
            # Build nested structure
            champion_raw = ChampionRaw(
                metadata=self._build_metadata(item),
                structure=self._build_structure(item),
                key_facts=self._build_key_facts(item),
            )

            spider.logger.info(f"Validated champion: {champion_raw.structure.name}")
            return champion_raw.model_dump(mode="json")

        except ValidationError as e:
            spider.logger.warning(
                f"Validation failed for {item.get('source_url', 'unknown')}: "
                f"{e.error_count()} errors"
            )
            # Log individual errors
            for error in e.errors():
                spider.logger.debug(f"  - {error['loc']}: {error['msg']}")

            # Return partial data for debugging
            return {
                "source_url": item.get("source_url"),
                "name": item.get("name"),
                "validation_errors": [str(e) for e in e.errors()],
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
                relations.append(Relation(
                    champion_name=rel.get("champion_name", ""),
                    source_url=rel.get("source_url", ""),
                    relationship_description=rel.get("relationship_description", ""),
                ))

        # Parse release date
        release_date = self._parse_date(item.get("release_date"))

        return Structure(
            name=item.get("name", "Unknown"),
            quote=item.get("quote", ""),
            biography=item.get("biography", ""),
            background=item.get("background", ""),
            appearance=item.get("appearance", ""),
            personality=item.get("personality", ""),
            abilities=self._parse_abilities(item.get("abilities", "")),
            relations=relations,
            relevant_links=item.get("relevant_links", []),
            trivia=item.get("trivia", ""),
            role=item.get("role", "Unknown"),
            release_date=release_date,
        )

    def _build_key_facts(self, item: dict) -> KeyFacts:
        """Build KeyFacts from item."""
        return KeyFacts(
            titles=Titles(
                real_name=item.get("real_name", "Unknown"),
                alias=item.get("alias", []),
            ),
            characteristics=Characteristics(
                species=item.get("species", "Unknown"),
                pronoun=item.get("pronoun", []),
                age=Age(
                    current=item.get("age_current", "Unknown"),
                    born_time=item.get("age_born_time", "Unknown"),
                ),
                weapons=item.get("weapons", "Unknown"),
            ),
            personal_status=PersonalStatus(
                status=item.get("status", "Unknown"),
                place_of_origin=item.get("place_of_origin", "Unknown"),
                current_residence=item.get("current_residence", "Unknown"),
                family=item.get("family", "Unknown"),
            ),
            professional_status=ProfessionalStatus(
                occupations=item.get("occupations", "Unknown"),
                regions=item.get("regions", "Unknown"),
                factions=item.get("factions", "Unknown"),
            ),
        )

    def _parse_date(self, date_str: str | None) -> datetime:
        """Parse date string or return default."""
        if not date_str:
            return datetime(2009, 10, 27)  # LoL release date as default

        # Try common date formats
        formats = ["%Y-%m-%d", "%B %d, %Y", "%d %B %Y", "%Y"]
        for fmt in formats:
            try:
                return datetime.strptime(date_str.strip(), fmt)
            except ValueError:
                continue

        return datetime(2009, 10, 27)

    def _parse_abilities(self, abilities_data: Any) -> list[str]:
        """Parse abilities into list of strings."""
        if isinstance(abilities_data, list):
            return abilities_data
        if isinstance(abilities_data, str):
            # If HTML content, return as single item for markdown conversion
            return [abilities_data] if abilities_data else []
        return []
```

### Step 3: Update settings.py to enable pipeline

```python
# In settings.py, uncomment/update:
ITEM_PIPELINES = {
    "src.scraper.pipelines.PydanticValidationPipeline": 300,
}
```

### Step 4: Update spider to use ItemLoader (optional enhancement)

If using ItemLoader in spider:

```python
from src.scraper.loaders import ChampionLoader

def parse(self, response, champion_name: str = None):
    loader = ChampionLoader(response=response)

    loader.add_value("source_url", response.url)
    loader.add_xpath("name", '//h1[contains(@class, "mw-page-title-main")]/text()')
    # ... rest of fields

    yield loader.load_item()
```

---

## Todo List

- [ ] Create `src/scraper/loaders.py` with ChampionLoader
- [ ] Implement text processing functions (strip, clean, remove_edit_markers)
- [ ] Update `src/scraper/pipelines.py` with full implementation
- [ ] Implement `_build_metadata()` method
- [ ] Implement `_build_structure()` method with Relation parsing
- [ ] Implement `_build_key_facts()` method
- [ ] Implement `_parse_date()` helper
- [ ] Implement `_parse_abilities()` helper
- [ ] Enable pipeline in `settings.py`
- [ ] Test with single champion
- [ ] Verify JSON output matches ChampionRaw schema

---

## Success Criteria

- [ ] Pipeline transforms flat item → nested ChampionRaw
- [ ] All required fields validated
- [ ] Validation errors logged (not crashing)
- [ ] JSON output has correct nested structure
- [ ] Dates parsed correctly
- [ ] Relations list properly structured

---

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Required field missing | High | Medium | Use "Unknown" defaults |
| Date parsing failures | Medium | Low | Default to LoL release date |
| Pydantic version mismatch | Low | High | Pin pydantic>=2.12.5 |
| Deep nesting serialization | Low | Medium | Use model_dump(mode="json") |

---

## Security Considerations

- No sensitive data processing
- Validation prevents malformed data injection
- Error messages don't expose internal paths

---

## Next Steps

After completing this phase:
1. Proceed to [Phase 04: Markdown Conversion](./phase-04-markdown-conversion.md)
2. Add HTML→markdown processing for content fields
