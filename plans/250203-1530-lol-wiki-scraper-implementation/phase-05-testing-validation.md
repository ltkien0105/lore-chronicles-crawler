# Phase 05: Testing & Validation

## Context Links

- [Main Plan](./plan.md)
- [Phase 04: Markdown Conversion](./phase-04-markdown-conversion.md)
- [ChampionRaw Model](../src/models/champion_raw.py)
- [HTML Structure Research](./research/researcher-01-html-structure.md)

---

## Overview

| Field | Value |
|-------|-------|
| Priority | High |
| Status | **DONE** |
| Completed | 2026-02-03 |
| Description | Test spider with 3 champions, validate output quality, fix edge cases |

---

## Key Insights

### Target Champions (Diverse Test Cases)

| Champion | Test Focus |
|----------|------------|
| **Cho'Gath** | Baseline - standard format, Void creature |
| **Kai'Sa** | Complex relations (father Kassadin), human backstory |
| **Darius** | Noxian faction, military role, detailed lore |

### Known Variations

- **Kai'Sa**: Uses "Alias(es)" plural label
- **Darius**: More detailed faction/region info
- **Cho'Gath**: Non-human species, minimal family info

---

## Requirements

### Functional
- Crawl all 3 champions without errors
- All ChampionRaw fields populated (or explicit "Unknown")
- JSON files generated in `output/` directory
- Markdown content is readable and clean

### Non-Functional
- No 429 (rate limit) errors
- Crawl completes in <2 minutes
- Log shows validation success for each champion

---

## Architecture

### Test Flow

```
1. Run spider with all 3 champions
    ↓
2. Verify JSON files created
    ↓
3. Validate JSON structure against ChampionRaw
    ↓
4. Manual review of content quality
    ↓
5. Fix issues and re-run
```

### Output Files

```
output/
├── cho_gath.json
├── kai_sa.json
└── darius.json
```

---

## Related Code Files

### Files to Create
- `tests/test_spider.py` - Spider unit tests
- `scripts/validate_output.py` - JSON validation script

### Files to Reference
- `src/scraper/spiders/lol_wiki_spider.py`
- `src/scraper/pipelines.py`
- `src/models/champion_raw.py`

---

## Implementation Steps

### Step 1: Create test script

Create `scripts/validate_output.py`:

```python
"""
Validate spider output JSON files against ChampionRaw model.
"""
import json
import sys
from pathlib import Path
from pydantic import ValidationError

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.models.champion_raw import ChampionRaw


def validate_json_file(filepath: Path) -> tuple[bool, list[str]]:
    """
    Validate a JSON file against ChampionRaw model.

    Returns:
        (is_valid, list of error messages)
    """
    errors = []

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return False, [f"JSON parse error: {e}"]

    # Handle both single item and list output
    items = data if isinstance(data, list) else [data]

    for i, item in enumerate(items):
        try:
            ChampionRaw.model_validate(item)
        except ValidationError as e:
            for err in e.errors():
                errors.append(f"Item {i}: {err['loc']} - {err['msg']}")

    return len(errors) == 0, errors


def check_content_quality(filepath: Path) -> list[str]:
    """
    Check content quality (non-validation checks).

    Returns:
        List of warning messages
    """
    warnings = []

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    items = data if isinstance(data, list) else [data]

    for item in items:
        name = item.get("structure", {}).get("name", "Unknown")

        # Check for empty required content
        structure = item.get("structure", {})
        if not structure.get("background"):
            warnings.append(f"{name}: Missing background content")
        if not structure.get("quote"):
            warnings.append(f"{name}: Missing quote")

        # Check for HTML artifacts
        for field in ["background", "appearance", "personality"]:
            content = structure.get(field, "")
            if "<" in content and ">" in content:
                warnings.append(f"{name}: {field} may contain HTML tags")

        # Check relations
        relations = structure.get("relations", [])
        if len(relations) == 0:
            warnings.append(f"{name}: No relations extracted")

    return warnings


def main():
    output_dir = Path("output")

    if not output_dir.exists():
        print("ERROR: output/ directory not found")
        return 1

    json_files = list(output_dir.glob("*.json"))

    if not json_files:
        print("ERROR: No JSON files in output/")
        return 1

    all_valid = True

    for filepath in json_files:
        print(f"\n{'='*50}")
        print(f"Validating: {filepath.name}")
        print("="*50)

        # Validate structure
        is_valid, errors = validate_json_file(filepath)

        if is_valid:
            print("  [PASS] Pydantic validation passed")
        else:
            print("  [FAIL] Pydantic validation failed:")
            for err in errors:
                print(f"    - {err}")
            all_valid = False

        # Check content quality
        warnings = check_content_quality(filepath)
        if warnings:
            print("  [WARN] Content quality issues:")
            for warn in warnings:
                print(f"    - {warn}")

    print(f"\n{'='*50}")
    if all_valid:
        print("All files validated successfully!")
        return 0
    else:
        print("Validation failed for some files")
        return 1


if __name__ == "__main__":
    sys.exit(main())
```

### Step 2: Create unit tests

Create `tests/test_spider.py`:

```python
"""
Unit tests for LOL Wiki spider.
"""
import pytest
from scrapy.http import HtmlResponse, Request

from src.scraper.spiders.lol_wiki_spider import LolWikiSpider
from src.scraper.markdown_converter import html_to_markdown, clean_markdown


class TestLolWikiSpider:
    """Tests for LolWikiSpider."""

    def test_spider_name(self):
        spider = LolWikiSpider()
        assert spider.name == "lol_wiki"

    def test_allowed_domains(self):
        spider = LolWikiSpider()
        assert "wiki.leagueoflegends.com" in spider.allowed_domains

    def test_default_champions(self):
        spider = LolWikiSpider()
        assert len(spider.champion_names) == 3
        assert "Cho'Gath" in spider.champion_names

    def test_custom_champions(self):
        spider = LolWikiSpider(champion_names="Ahri,Yasuo")
        assert spider.champion_names == ["Ahri", "Yasuo"]

    def test_start_requests_count(self):
        spider = LolWikiSpider()
        requests = list(spider.start_requests())
        assert len(requests) == 3


class TestMarkdownConverter:
    """Tests for markdown conversion utilities."""

    def test_html_to_markdown_paragraph(self):
        html = "<p>This is a test paragraph.</p>"
        md = html_to_markdown(html)
        assert "This is a test paragraph." in md
        assert "<p>" not in md

    def test_html_to_markdown_link(self):
        html = '<p>See <a href="/en-us/Universe:Ahri">Ahri</a> for more.</p>'
        md = html_to_markdown(html)
        assert "[Ahri]" in md
        assert "(" in md

    def test_html_to_markdown_list(self):
        html = "<ul><li>Item 1</li><li>Item 2</li></ul>"
        md = html_to_markdown(html)
        assert "Item 1" in md
        assert "Item 2" in md

    def test_clean_markdown_edit_markers(self):
        text = "Background [edit]\nSome content here."
        cleaned = clean_markdown(text)
        assert "[edit]" not in cleaned

    def test_clean_markdown_excessive_newlines(self):
        text = "Line 1\n\n\n\n\nLine 2"
        cleaned = clean_markdown(text)
        assert "\n\n\n" not in cleaned

    def test_empty_input(self):
        assert html_to_markdown("") == ""
        assert html_to_markdown(None) == ""
        assert clean_markdown("") == ""


class TestExtraction:
    """Tests for data extraction (requires mock response)."""

    @pytest.fixture
    def mock_response(self):
        """Create mock response with sample wiki HTML."""
        html = """
        <html>
        <body>
            <h1 class="mw-page-title-main">Darius</h1>
            <blockquote>They will regret opposing me.</blockquote>
            <table class="infobox">
                <tr><th>Real Name</th><td>Darius</td></tr>
                <tr><th>Species</th><td>Human</td></tr>
                <tr><th>Status</th><td>Alive</td></tr>
            </table>
            <h2 id="Background">Background</h2>
            <p>Darius is a commander in the Noxian army.</p>
            <p>He leads with brutal efficiency.</p>
            <h2 id="Appearance">Appearance</h2>
            <p>A tall, muscular man with a massive axe.</p>
        </body>
        </html>
        """
        url = "https://wiki.leagueoflegends.com/en-us/Universe:Darius"
        request = Request(url=url)
        return HtmlResponse(url=url, request=request, body=html.encode())

    def test_extract_name(self, mock_response):
        spider = LolWikiSpider()
        name = spider._extract_name(mock_response)
        assert name == "Darius"

    def test_extract_quote(self, mock_response):
        spider = LolWikiSpider()
        quote = spider._extract_quote(mock_response)
        assert "regret opposing me" in quote

    def test_extract_infobox_field(self, mock_response):
        spider = LolWikiSpider()
        species = spider._extract_infobox_field(mock_response, "Species")
        assert species == "Human"
```

### Step 3: Run full crawl

```bash
cd D:\Development\Projects\Python\lore-chronicles-crawler

# Run spider with all 3 champions
scrapy crawl lol_wiki -o output/champions.json

# Or run per-champion for debugging
scrapy crawl lol_wiki -a champion_names="Darius" -o output/darius.json
scrapy crawl lol_wiki -a champion_names="Kai'Sa" -o output/kai_sa.json
scrapy crawl lol_wiki -a champion_names="Cho'Gath" -o output/cho_gath.json
```

### Step 4: Validate output

```bash
python scripts/validate_output.py
```

### Step 5: Run unit tests

```bash
pytest tests/test_spider.py -v
```

### Step 6: Manual content review

Check each JSON file for:
- [ ] Name is correct
- [ ] Quote is present and sensible
- [ ] Background has multiple paragraphs
- [ ] Abilities list is populated
- [ ] Relations contain valid champion names and URLs
- [ ] No HTML tags in markdown fields

---

## Todo List

- [ ] Create `scripts/validate_output.py`
- [ ] Create `tests/test_spider.py`
- [ ] Run crawl for Darius (simplest)
- [ ] Validate Darius output
- [ ] Fix any extraction issues
- [ ] Run crawl for Kai'Sa (complex relations)
- [ ] Validate Kai'Sa output
- [ ] Run crawl for Cho'Gath (non-human)
- [ ] Validate Cho'Gath output
- [ ] Run full crawl with all 3 champions
- [ ] Run unit tests
- [ ] Manual review of content quality
- [ ] Document any remaining issues

---

## Success Criteria

- [ ] All 3 champions crawled without errors
- [ ] All JSON files pass Pydantic validation
- [ ] No HTML tags in markdown content
- [ ] Relations extracted with valid URLs
- [ ] Quote extracted for each champion
- [ ] Background section has substantial content
- [ ] No 429 rate limit errors during crawl
- [ ] Unit tests pass

---

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Rate limiting during full crawl | Medium | Medium | 2s delay, AutoThrottle |
| Wiki structure changed | Low | High | Re-run HTML analysis |
| Some fields missing | High | Low | Accept "Unknown" defaults |
| Test data differs from production | Medium | Medium | Test with real wiki pages |

---

## Security Considerations

- No credentials in test scripts
- Output files don't contain sensitive data
- Validation script runs locally only

---

## Next Steps

After completing this phase:
1. Review all generated JSON files
2. Create summary report of extraction quality
3. Document any fields that need manual review
4. Consider adding more champions to test set
5. Create CI/CD pipeline for automated testing (future phase)

---

## Validation Checklist

### Per-Champion Checks

#### Darius
- [ ] Name: "Darius"
- [ ] Quote: Present
- [ ] Species: "Human"
- [ ] Status: "Alive"
- [ ] Regions: Contains "Noxus"
- [ ] Background: Multiple paragraphs
- [ ] Relations: Draven mentioned

#### Kai'Sa
- [ ] Name: "Kai'Sa"
- [ ] Quote: Present
- [ ] Species: "Human" or "Void-touched"
- [ ] Relations: Kassadin (father)
- [ ] Background: Void survival story

#### Cho'Gath
- [ ] Name: "Cho'Gath"
- [ ] Quote: Present
- [ ] Species: "Void" or "Voidborn"
- [ ] Status: "Alive"
- [ ] Abilities: Extracted
- [ ] Background: Void origin story
