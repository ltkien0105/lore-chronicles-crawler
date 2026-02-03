# Phase 02: Spider Implementation

## Context Links

- [Main Plan](./plan.md)
- [Phase 01: Setup](./phase-01-scrapy-project-setup.md)
- [HTML Structure Research](./research/researcher-01-html-structure.md)
- [Scrapy Patterns Research](./research/researcher-02-scrapy-patterns.md)

---

## Overview

| Field | Value |
|-------|-------|
| Priority | High |
| Status | pending |
| Description | Implement core spider with XPath/CSS selectors for all ChampionRaw fields |

---

## Key Insights

### From HTML Structure Research

1. **Page structure is 100% consistent** across all champion pages
2. **Champion name**: `h1.mw-page-title-main` (high confidence)
3. **Quote**: `blockquote` element or `.infobox-quote`
4. **Infobox**: Table structure with label/value pairs in adjacent `<td>` elements
5. **Content sections**: `<h2>` with `id` attribute, content in following `<p>` tags
6. **Relations**: Links matching `/Universe:` in href

### Critical Selectors

| Field | Primary XPath | Reliability |
|-------|---------------|-------------|
| Name | `//h1[@class='mw-page-title-main']/text()` | 100% |
| Quote | `//blockquote[1]` | 100% |
| Background | `//h2[@id='Background']/following-sibling::p` | 100% |
| Relations | `//a[starts-with(@href, '/en-us/Universe:')]` | 100% |
| Infobox row | `//th[contains(text(), 'Label')]/following-sibling::td` | 95% |

---

## Requirements

### Functional
- Extract all fields defined in `ChampionRaw` model
- Handle variations in infobox labels (e.g., "Alias" vs "Alias(es)")
- Extract content between `<h2>` headings
- Capture all Universe links for relations
- Pass raw HTML sections to ItemLoader for markdown conversion

### Non-Functional
- Single spider class handling all champion pages
- Start URLs configurable
- Graceful handling of missing optional fields

---

## Architecture

### Spider Flow

```
start_requests()
    ↓
parse(response)
    ├─→ Extract name, quote (direct selectors)
    ├─→ Parse infobox table (key-value extraction)
    ├─→ Extract content sections (Background, Appearance, etc.)
    ├─→ Extract relations (Universe links with context)
    └─→ yield ChampionItem
```

### Helper Methods

```
_extract_infobox_field(response, label) → str
_extract_section_html(response, section_id) → str
_extract_relations(response) → list[dict]
_extract_abilities_list(response) → list[str]
```

---

## Related Code Files

### Files to Create
- `src/scraper/spiders/lol_wiki_spider.py`

### Files to Reference
- `src/scraper/items.py` - ChampionItem class
- `src/utils/constants.py` - UNIVERSE_WIKI constant
- `research/researcher-01-html-structure.md` - Selector patterns

---

## Implementation Steps

### Step 1: Create spider file

Create `src/scraper/spiders/lol_wiki_spider.py`:

```python
"""
LOL Wiki Universe Spider - Extracts champion lore data.
"""
import scrapy
from urllib.parse import urljoin, unquote

from src.scraper.items import ChampionItem
from src.utils.constants import BASE_URL_WIKI, UNIVERSE_WIKI


class LolWikiSpider(scrapy.Spider):
    name = "lol_wiki"
    allowed_domains = ["wiki.leagueoflegends.com"]

    # Default champions to crawl
    champion_names = ["Cho'Gath", "Kai'Sa", "Darius"]

    def start_requests(self):
        """Generate initial requests for champion pages."""
        for champion in self.champion_names:
            url = f"{UNIVERSE_WIKI}{champion}"
            yield scrapy.Request(
                url,
                callback=self.parse,
                cb_kwargs={"champion_name": champion}
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
        item["abilities"] = self._extract_abilities_html(response)
        item["trivia"] = self._extract_section_html(response, "Trivia")

        # Relations and links
        item["relations"] = self._extract_relations(response)
        item["relevant_links"] = self._extract_relevant_links(response)

        # Role and release date (may not be on Universe page)
        item["role"] = self._extract_infobox_field(response, "Role")
        item["release_date"] = self._extract_infobox_field(response, "Release")

        # === Key Facts - Titles ===
        item["real_name"] = self._extract_infobox_field(response, "Real Name")
        item["alias"] = self._extract_infobox_list(response, "Alias")

        # === Key Facts - Characteristics ===
        item["species"] = self._extract_infobox_field(response, "Species")
        item["pronoun"] = self._extract_infobox_list(response, "Pronoun")
        item["age_current"] = self._extract_infobox_field(response, "Age")
        item["age_born_time"] = self._extract_infobox_field(response, "Born")
        item["weapons"] = self._extract_infobox_field(response, "Weapon")

        # === Key Facts - Personal Status ===
        item["status"] = self._extract_infobox_field(response, "Status")
        item["place_of_origin"] = self._extract_infobox_field(response, "Origin")
        item["current_residence"] = self._extract_infobox_field(response, "Residence")
        item["family"] = self._extract_infobox_field(response, "Family")

        # === Key Facts - Professional Status ===
        item["occupations"] = self._extract_infobox_field(response, "Occupation")
        item["regions"] = self._extract_infobox_field(response, "Region")
        item["factions"] = self._extract_infobox_field(response, "Faction")

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
        # Try blockquote first
        quote = response.xpath('//blockquote[1]//text()').getall()
        if quote:
            return " ".join(q.strip() for q in quote if q.strip())

        # Fallback: infobox quote
        quote = response.css('.infobox-quote::text').get()
        return quote.strip() if quote else ""

    def _extract_biography_link(self, response) -> str:
        """Extract link to full biography page."""
        bio_link = response.xpath(
            '//a[contains(text(), "Biography") or contains(text(), "Read Bio")]/@href'
        ).get()
        if bio_link:
            return urljoin(BASE_URL_WIKI, bio_link)
        return ""

    def _extract_section_html(self, response, section_id: str) -> str:
        """Extract HTML content between h2 section and next h2."""
        # Find all content after the h2 until next h2
        paragraphs = response.xpath(
            f'//h2[contains(@id, "{section_id}") or '
            f'.//span[@id="{section_id}"]]/following-sibling::*'
            f'[self::p or self::ul or self::ol or self::dl]'
            f'[preceding-sibling::h2[1][contains(@id, "{section_id}") or '
            f'.//span[@id="{section_id}"]]]'
        ).getall()

        if not paragraphs:
            # Alternative: simpler selector
            paragraphs = response.xpath(
                f'//h2[@id="{section_id}"]/following-sibling::p'
            ).getall()

        return "\n".join(paragraphs) if paragraphs else ""

    def _extract_abilities_html(self, response) -> str:
        """Extract abilities section (may be h2 or h3)."""
        # Try h2 first
        content = self._extract_section_html(response, "Abilities")
        if content:
            return content

        # Try h3 within another section
        abilities = response.xpath(
            '//h3[contains(text(), "Abilities")]/following-sibling::*'
            '[self::dl or self::ul or self::p]'
        ).getall()
        return "\n".join(abilities) if abilities else ""

    def _extract_relations(self, response) -> list:
        """Extract champion relations with URLs and context."""
        relations = []
        seen = set()

        # Find all Universe links
        for link in response.xpath('//a[contains(@href, "/Universe:")]'):
            href = link.xpath('./@href').get()
            if not href or href == response.url:
                continue

            # Extract champion name from URL
            champ_name = unquote(href.split(":")[-1].replace("_", " "))
            if champ_name in seen:
                continue
            seen.add(champ_name)

            # Get surrounding context (parent paragraph text)
            context = link.xpath(
                './ancestor::li[1]//text() | ./ancestor::p[1]//text()'
            ).getall()
            description = " ".join(c.strip() for c in context if c.strip())

            relations.append({
                "champion_name": champ_name,
                "source_url": urljoin(BASE_URL_WIKI, href),
                "relationship_description": description[:200] if description else ""
            })

        return relations

    def _extract_relevant_links(self, response) -> list:
        """Extract all relevant Universe and story links."""
        links = []
        for href in response.xpath('//a[contains(@href, "/Universe:")]/@href').getall():
            full_url = urljoin(BASE_URL_WIKI, href)
            if full_url not in links and full_url != response.url:
                links.append(full_url)
        return links

    def _extract_infobox_field(self, response, label: str) -> str:
        """Extract single value from infobox table row."""
        # Try th/td pattern
        value = response.xpath(
            f'//th[contains(text(), "{label}")]/following-sibling::td//text()'
        ).getall()
        if value:
            return " ".join(v.strip() for v in value if v.strip())

        # Try td/td pattern (some infoboxes use this)
        value = response.xpath(
            f'//td[contains(text(), "{label}")]/following-sibling::td//text()'
        ).getall()
        return " ".join(v.strip() for v in value if v.strip()) if value else ""

    def _extract_infobox_list(self, response, label: str) -> list:
        """Extract list values from infobox (e.g., aliases, pronouns)."""
        # Get all text from the cell
        values = response.xpath(
            f'//th[contains(text(), "{label}")]/following-sibling::td//text()'
        ).getall()

        if not values:
            values = response.xpath(
                f'//td[contains(text(), "{label}")]/following-sibling::td//text()'
            ).getall()

        # Clean and split by common separators
        cleaned = []
        for v in values:
            v = v.strip()
            if v and v not in [",", "/", "|"]:
                cleaned.append(v)

        return cleaned
```

### Step 2: Add custom command for champion list

Optionally override champion list via command line:

```bash
scrapy crawl lol_wiki -a champion_names="Ahri,Yasuo,Jinx"
```

Update spider `__init__`:

```python
def __init__(self, champion_names=None, *args, **kwargs):
    super().__init__(*args, **kwargs)
    if champion_names:
        self.champion_names = [c.strip() for c in champion_names.split(",")]
```

### Step 3: Test spider with single champion

```bash
scrapy crawl lol_wiki -a champion_names="Darius" -o output/test.json
```

---

## Todo List

- [ ] Create `src/scraper/spiders/lol_wiki_spider.py`
- [ ] Implement `start_requests()` with configurable champion list
- [ ] Implement `parse()` method extracting all ChampionItem fields
- [ ] Implement `_extract_name()` with fallback
- [ ] Implement `_extract_quote()` with blockquote and infobox fallback
- [ ] Implement `_extract_section_html()` for content sections
- [ ] Implement `_extract_relations()` with URL and context
- [ ] Implement `_extract_infobox_field()` for single values
- [ ] Implement `_extract_infobox_list()` for list values
- [ ] Test with single champion (`Darius`)
- [ ] Verify all fields populated

---

## Success Criteria

- [ ] Spider runs without XPath/CSS errors
- [ ] Name, quote extracted correctly for all 3 champions
- [ ] Infobox fields extracted (species, status, etc.)
- [ ] Content sections captured as HTML strings
- [ ] Relations list populated with champion links
- [ ] JSON output contains all expected fields

---

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| XPath mismatches on edge cases | Medium | Medium | Use `contains()` for flexible matching |
| Missing sections on some pages | Low | Low | Return empty string, handle in pipeline |
| Relation context too long | Low | Low | Truncate to 200 chars |
| Encoding issues with special chars | Medium | Medium | Use `unquote()` for URL decoding |

---

## Security Considerations

- No credentials or secrets in spider code
- URLs constructed from trusted constants
- User input (champion_names) sanitized via URL encoding

---

## Next Steps

After completing this phase:
1. Proceed to [Phase 03: Item Loaders & Processors](./phase-03-item-loaders-processors.md)
2. Add markdown conversion and Pydantic validation
