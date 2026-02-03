---
title: LOL Wiki Scrapy Spider Implementation
description: Build Scrapy spider to crawl League of Legends Wiki Universe pages and extract champion lore data into structured Pydantic models
status: pending
priority: high
effort: medium
branch: feature/lol-wiki-scraper
tags: [scrapy, web-scraping, pydantic, mediawiki, lol]
created: 2025-02-03
---

# LOL Wiki Scrapy Spider Implementation Plan

## Overview

Implement a Scrapy-based spider to crawl League of Legends Wiki Universe pages, extracting champion lore data into `ChampionRaw` Pydantic models with markdown-formatted content sections.

## Target URLs

- `https://wiki.leagueoflegends.com/en-us/Universe:Cho'Gath`
- `https://wiki.leagueoflegends.com/en-us/Universe:Kai'Sa`
- `https://wiki.leagueoflegends.com/en-us/Universe:Darius`

## Research References

- [HTML Structure Analysis](./research/researcher-01-html-structure.md)
- [Scrapy + Pydantic Patterns](./research/researcher-02-scrapy-patterns.md)

## Phases

| # | Phase | Status | Description |
|---|-------|--------|-------------|
| 1 | [Project Setup](./phase-01-scrapy-project-setup.md) | **DONE** | Initialize Scrapy project in `src/scraper/` |
| 2 | [Spider Implementation](./phase-02-spider-implementation.md) | **DONE** | Core spider with XPath/CSS selectors |
| 3 | [Item Loaders](./phase-03-item-loaders-processors.md) | **DONE** | ItemLoader + Pydantic validation pipeline |
| 4 | [Markdown Conversion](./phase-04-markdown-conversion.md) | pending | HTML→markdown for content sections |
| 5 | [Testing & Validation](./phase-05-testing-validation.md) | pending | Test with 3 champions, output JSON |

## Key Dependencies

- `scrapy>=2.14.1` - Spider framework
- `pydantic>=2.12.5` - Data validation (existing model)
- `markdownify>=0.14.0` - HTML→markdown conversion (ADD)
- `beautifulsoup4>=4.14.3` - Fallback HTML parsing

## Output Structure

```
output/
├── cho_gath.json
├── kai_sa.json
└── darius.json
```

## Architecture

```
src/scraper/
├── __init__.py
├── spiders/
│   ├── __init__.py
│   └── lol_wiki_spider.py
├── items.py          # Scrapy Item definitions (minimal)
├── loaders.py        # ItemLoader + processors
├── pipelines.py      # Pydantic validation pipeline
├── middlewares.py    # (default Scrapy)
└── settings.py       # AutoThrottle config
```

## Success Criteria

- [ ] Spider crawls 3 target champions without errors
- [ ] All `ChampionRaw` fields populated correctly
- [ ] Content sections converted to clean markdown
- [ ] Relations extracted with URLs
- [ ] Rate limiting prevents 429 errors
- [ ] JSON output files generated per champion

## Risks

| Risk | Mitigation |
|------|------------|
| Wiki structure changes | Use flexible XPath with `contains()` |
| Rate limiting (429) | AutoThrottle + 2s delay minimum |
| Missing optional fields | Pydantic defaults + graceful handling |

---

## Validation Summary

**Validated:** 2025-02-03
**Questions asked:** 5

### Confirmed Decisions
- **Scraping framework**: Scrapy (not crawl4ai/LLM extraction)
- **Missing fields (role, release_date)**: Use default string "Unknown"
- **Abilities format**: `list[str]` containing ability names only
- **Output format**: Single `champions.json` file
- **Model fix**: Remove duplicate `abilities` field, keep `list[str]` version (line 63-65)

### Action Items
- [ ] Fix ChampionRaw model: Remove duplicate `abilities: str` field (line 42-45)
- [ ] Update settings.py: Output to single `output/champions.json`
- [ ] Update phase-03: Use "Unknown" string defaults for role/release_date
