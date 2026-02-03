# Scrapy + Pydantic Integration: Best Practices Research Report

**Date**: 2025-02-03
**Focus**: Structured data extraction for MediaWiki-based wiki scraping

---

## 1. Scrapy Architecture for Wiki Scraping

### Request-Response Pipeline
- **HtmlResponse** auto-detects encoding from meta tags (critical for wiki content)
- **Metadata carryover**: Use `cb_kwargs` to pass champion names, URLs through callbacks
- **LinkExtractor** for normalized URL handling across MediaWiki structure

### ItemLoader Pattern
```python
from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose, TakeFirst

loader = ItemLoader()
loader.add_xpath('name', '//h1[@class="mw-page-title-main"]/text()')
loader.add_xpath('abilities',
    '//h3[contains(text(),"Abilities")]/..//dl/dt/strong/text()',
    MapCompose(str.strip))
item_dict = loader.load_item()
```

**Key Pattern**: Combine MapCompose for field processing + Pydantic for validation.

---

## 2. Pydantic + Scrapy Integration

### Validation Strategy (Recommended)
```python
from pydantic import BaseModel, Field, ValidationError

class Champion(BaseModel):
    name: str
    lore: str | None = None
    abilities: list[str] = Field(default_factory=list)
    related_champions: list[str] = Field(default_factory=list)

    class Config:
        validate_assignment = True

# Usage in spider
try:
    champ = Champion(**loader.load_item())
    yield champ.model_dump_json()
except ValidationError as e:
    self.logger.error(f"Validation failed: {e}, url={response.url}")
```

### Nested Models Pattern
```python
class Relation(BaseModel):
    champion_name: str
    relation_type: str  # 'ally', 'rival', 'family'

class ChampionFull(BaseModel):
    name: str
    relations: list[Relation] = Field(default_factory=list)
```

**Advantage**: Type-safe extraction with zero boilerplate error handling.

---

## 3. MediaWiki-Specific Best Practices

### Structural Consistency
- Infobox always in `.infobox` table class
- Main content in `.mw-content-container > .mw-parser-output`
- Use `id` attributes on headings (e.g., `h2#Background`)

### Normalized Link Extraction
```python
from urllib.parse import urlparse, unquote

def normalize_champion_url(url: str) -> str:
    # Handle: /wiki/Ahri, /en-us/Universe:Ahri
    path = urlparse(url).path.split('/')[-1]
    return unquote(path).replace('_', ' ')
```

---

## 4. Rate Limiting Configuration

### Critical Settings
```python
# settings.py
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 10
DOWNLOAD_DELAY = 2
CONCURRENT_REQUESTS_PER_DOMAIN = 1
RANDOMIZE_DOWNLOAD_DELAY = True
RETRY_TIMES = 3
RETRY_HTTP_CODES = [500, 502, 503, 504, 429]
```

**Why**: MediaWiki respects robots.txt; AutoThrottle prevents 429 (Too Many Requests) errors.

---

## 5. HTML-to-Markdown Conversion

### Library Recommendations

| Library | Use Case | Verdict |
|---------|----------|---------|
| **markdownify** | Lore preservation | ✓ Use for this project |
| **html2text** | Dense extraction | Alternative if links matter |
| **pypandoc** | Professional quality | Overkill for wiki content |

### Implementation
```python
from markdownify import markdownify as md

# Extract content sections
content_html = response.xpath(
    '//h2[@id="Background"]/following-sibling::p'
).getall()

lore_md = '\n\n'.join(md(html, heading_style="ATX") for html in content_html)
# Clean: '\n\n'.join(p for p in lore_md.split('\n\n') if p.strip())
```

**Preference**: **markdownify** preserves heading hierarchy and link structure.

---

## 6. Champion Relationship Extraction

### Two-Stage Extraction

**Stage 1: Direct Links**
```python
# Extract all Universe links
related_urls = response.xpath(
    '//a[contains(@href, "/Universe:") or contains(@href, "/wiki/")]/@href'
).getall()
related_champions = [normalize_champion_url(url) for url in related_urls]
```

**Stage 2: Relation Type Inference**
```python
# Check link context
for link in response.xpath('//a[contains(@href, "/wiki/")]'):
    text = ' '.join(link.xpath('.//ancestor::p[1]//text()').getall()).lower()
    if any(word in text for word in ['ally', 'partner', 'together']):
        relation_type = 'ally'
    elif any(word in text for word in ['enemy', 'rival', 'opposes']):
        relation_type = 'rival'
    else:
        relation_type = 'related'
```

---

## 7. Error Handling Pattern

```python
from pydantic import ValidationError

class ChampionSpider(scrapy.Spider):
    def parse_champion(self, response):
        loader = ItemLoader(response=response)
        # ... extraction code ...

        try:
            champ = Champion(**loader.load_item())
            yield champ
        except ValidationError as e:
            self.logger.warning(
                f"Extraction failed for {response.url}: {e.error_count()} errors"
            )
            # Partial success: extract what we can
            yield {'url': response.url, 'errors': str(e)}
```

---

## 8. Dependencies Summary

```toml
scrapy = ">=2.14.1"
pydantic = ">=2.12.5"
markdownify = ">=0.14.0"  # or 0.13.x
requests = ">=2.32.5"
beautifulsoup4 = ">=4.14.3"  # Fallback parsing
```

---

## Key Findings

✓ **Pydantic + ItemLoader**: Eliminates verbose validation code
✓ **Markdownify**: Best balance of structure preservation + simplicity
✓ **AutoThrottle**: Non-negotiable for wiki scraping (prevents bans)
✓ **Nested Models**: Handle complex relationships cleanly
✗ **Do NOT**: Use Scrapy's built-in `Item` classes (deprecated, Pydantic superior)

---

**Status**: Ready for implementation. Recommend using markdownify + Pydantic nested models for relations.
