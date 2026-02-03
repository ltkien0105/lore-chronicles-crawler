# Phase 01: Scrapy Project Setup

## Context Links

- [Main Plan](./plan.md)
- [Scrapy Patterns Research](./research/researcher-02-scrapy-patterns.md)
- [Existing Constants](../src/utils/constants.py) - `BASE_URL_WIKI`, `UNIVERSE_WIKI`

---

## Overview

| Field | Value |
|-------|-------|
| Priority | High |
| Status | **DONE** |
| Completed | 2025-02-03 |
| Description | Initialize Scrapy project structure in `src/scraper/` with rate limiting configuration |

---

## Key Insights

1. **MediaWiki respects robots.txt** - AutoThrottle essential to prevent 429 errors
2. **Pydantic over Scrapy Items** - Use minimal Item class, validation in pipeline
3. **Project location** - Place in `src/scraper/` to integrate with existing codebase
4. **markdownify dependency** - Must add to `pyproject.toml`

---

## Requirements

### Functional
- Initialize Scrapy project with correct structure
- Configure AutoThrottle for polite crawling
- Set up output directory for JSON files
- Integrate with existing `src/models/champion_raw.py`

### Non-Functional
- 2 second minimum delay between requests
- Max 1 concurrent request per domain
- Retry on 500, 502, 503, 504, 429 errors

---

## Architecture

```
lore-chronicles-crawler/
├── src/
│   ├── scraper/                    # NEW: Scrapy project root
│   │   ├── __init__.py
│   │   ├── spiders/
│   │   │   ├── __init__.py
│   │   │   └── lol_wiki_spider.py  # Phase 02
│   │   ├── items.py                # Minimal item definitions
│   │   ├── loaders.py              # Phase 03
│   │   ├── pipelines.py            # Phase 03
│   │   ├── middlewares.py          # Default (auto-generated)
│   │   └── settings.py             # AutoThrottle config
│   ├── models/
│   │   └── champion_raw.py         # EXISTING
│   └── utils/
│       └── constants.py            # EXISTING (BASE_URL_WIKI)
├── output/                         # NEW: JSON output directory
└── scrapy.cfg                      # NEW: Scrapy config file
```

---

## Related Code Files

### Files to Create
- `src/scraper/__init__.py`
- `src/scraper/spiders/__init__.py`
- `src/scraper/items.py`
- `src/scraper/middlewares.py`
- `src/scraper/pipelines.py`
- `src/scraper/settings.py`
- `scrapy.cfg`
- `output/.gitkeep`

### Files to Modify
- `pyproject.toml` - Add `markdownify>=0.14.0` dependency

### Files to Reference
- `src/models/champion_raw.py` - Pydantic model structure
- `src/utils/constants.py` - URL constants

---

## Implementation Steps

### Step 1: Add markdownify dependency

```bash
# In pyproject.toml, add to dependencies:
# "markdownify>=0.14.0",
```

### Step 2: Create output directory

```bash
mkdir -p output
touch output/.gitkeep
```

### Step 3: Create scrapy.cfg

```ini
[settings]
default = src.scraper.settings

[deploy]
project = lol_wiki_scraper
```

### Step 4: Create src/scraper/__init__.py

```python
# Scrapy project for LoL Wiki scraping
```

### Step 5: Create src/scraper/spiders/__init__.py

```python
# Spider package
```

### Step 6: Create src/scraper/settings.py

```python
BOT_NAME = "lol_wiki_scraper"

SPIDER_MODULES = ["src.scraper.spiders"]
NEWSPIDER_MODULE = "src.scraper.spiders"

# Crawl responsibly
ROBOTSTXT_OBEY = True
USER_AGENT = "LoreChroniclesCrawler/1.0 (+https://github.com/your-repo)"

# Rate limiting - CRITICAL for wiki scraping
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 2
AUTOTHROTTLE_MAX_DELAY = 10
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
DOWNLOAD_DELAY = 2
CONCURRENT_REQUESTS = 1
CONCURRENT_REQUESTS_PER_DOMAIN = 1
RANDOMIZE_DOWNLOAD_DELAY = True

# Retry configuration
RETRY_ENABLED = True
RETRY_TIMES = 3
RETRY_HTTP_CODES = [500, 502, 503, 504, 429]

# Output settings
FEED_EXPORT_ENCODING = "utf-8"
FEEDS = {
    "output/%(name)s.json": {
        "format": "json",
        "encoding": "utf8",
        "indent": 2,
        "overwrite": True,
    }
}

# Pipelines (enable in Phase 03)
ITEM_PIPELINES = {
    # "src.scraper.pipelines.PydanticValidationPipeline": 300,
}

# Logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s [%(name)s] %(levelname)s: %(message)s"
```

### Step 7: Create src/scraper/items.py

```python
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
```

### Step 8: Create src/scraper/middlewares.py

```python
"""
Scrapy middlewares - using defaults for now.
"""
from scrapy import signals


class LolWikiSpiderMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        return None

    def process_spider_output(self, response, result, spider):
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        pass

    def process_start_requests(self, start_requests, spider):
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info(f"Spider opened: {spider.name}")


class LolWikiDownloaderMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        return None

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        pass

    def spider_opened(self, spider):
        spider.logger.info(f"Spider opened: {spider.name}")
```

### Step 9: Create src/scraper/pipelines.py (stub)

```python
"""
Item pipelines for Pydantic validation.
Full implementation in Phase 03.
"""


class PydanticValidationPipeline:
    """Validates scraped items against ChampionRaw Pydantic model."""

    def process_item(self, item, spider):
        # Implementation in Phase 03
        return item
```

### Step 10: Verify setup

```bash
# From project root
cd D:\Development\Projects\Python\lore-chronicles-crawler
scrapy list  # Should show no spiders yet (added in Phase 02)
```

---

## Todo List

- [ ] Add `markdownify>=0.14.0` to pyproject.toml
- [ ] Create `output/.gitkeep`
- [ ] Create `scrapy.cfg`
- [ ] Create `src/scraper/__init__.py`
- [ ] Create `src/scraper/spiders/__init__.py`
- [ ] Create `src/scraper/settings.py` with AutoThrottle config
- [ ] Create `src/scraper/items.py` with ChampionItem
- [ ] Create `src/scraper/middlewares.py`
- [ ] Create `src/scraper/pipelines.py` (stub)
- [ ] Run `scrapy list` to verify configuration

---

## Success Criteria

- [ ] `scrapy list` runs without errors from project root
- [ ] All scraper module files exist
- [ ] AutoThrottle configured with 2s delay minimum
- [ ] markdownify available as dependency
- [ ] output directory ready for JSON files

---

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Module import path issues | Medium | High | Use absolute imports, verify with `scrapy list` |
| Missing dependency | Low | Medium | Add markdownify to pyproject.toml early |
| scrapy.cfg path incorrect | Medium | Medium | Test with `scrapy list` command |

---

## Security Considerations

- `USER_AGENT` identifies crawler politely
- `ROBOTSTXT_OBEY = True` respects site rules
- Rate limiting prevents abuse

---

## Next Steps

After completing this phase:
1. Proceed to [Phase 02: Spider Implementation](./phase-02-spider-implementation.md)
2. Create the actual spider with selectors based on HTML research
