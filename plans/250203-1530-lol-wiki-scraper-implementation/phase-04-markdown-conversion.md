# Phase 04: Markdown Conversion

## Context Links

- [Main Plan](./plan.md)
- [Phase 03: Item Loaders](./phase-03-item-loaders-processors.md)
- [Scrapy Patterns Research](./research/researcher-02-scrapy-patterns.md)

---

## Overview

| Field | Value |
|-------|-------|
| Priority | Medium |
| Status | pending |
| Description | Convert HTML content sections to clean markdown using markdownify |

---

## Key Insights

### From Scrapy Patterns Research

1. **markdownify** - Best library for preserving heading hierarchy and link structure
2. **Pipeline integration** - Convert HTML→markdown after extraction, before Pydantic validation
3. **Cleanup required** - Remove edit markers, empty paragraphs, excessive newlines

### Fields Requiring Conversion

| Field | Source Format | Target Format |
|-------|--------------|---------------|
| background | HTML `<p>` elements | Markdown paragraphs |
| appearance | HTML `<p>` elements | Markdown paragraphs |
| personality | HTML `<p>` elements | Markdown paragraphs |
| abilities | HTML `<dl>/<ul>` | Markdown list |
| trivia | HTML `<ul><li>` | Markdown bullet list |
| family | HTML with links | Markdown with links |
| occupations | HTML list | Markdown list |

---

## Requirements

### Functional
- Convert all HTML content fields to markdown
- Preserve internal wiki links as markdown links
- Convert `<ul>/<ol>` to markdown lists
- Convert `<strong>/<em>` to markdown formatting
- Strip unwanted elements (edit buttons, scripts)

### Non-Functional
- Clean, readable markdown output
- No HTML tags in final output
- Consistent heading levels (ATX style: `#`, `##`)

---

## Architecture

### Processing Order

```
Spider extracts HTML
    ↓
MarkdownConversionPipeline (priority 200)
    ├─ Convert HTML fields to markdown
    ├─ Clean up artifacts
    └─ Normalize links
    ↓
PydanticValidationPipeline (priority 300)
    └─ Validate and structure data
```

### Conversion Config

```python
markdownify_options = {
    "heading_style": "ATX",        # Use # for headings
    "bullets": "-",                 # Use - for lists
    "strip": ["script", "style", "span.mw-editsection"],
    "convert": ["a", "strong", "em", "p", "ul", "ol", "li", "dl", "dt", "dd"],
}
```

---

## Related Code Files

### Files to Create
- `src/scraper/markdown_converter.py` - Conversion utilities

### Files to Modify
- `src/scraper/pipelines.py` - Add MarkdownConversionPipeline
- `src/scraper/settings.py` - Enable new pipeline

### Files to Reference
- `src/utils/constants.py` - BASE_URL_WIKI for link normalization

---

## Implementation Steps

### Step 1: Create markdown_converter.py

```python
"""
HTML to Markdown conversion utilities.
"""
import re
from markdownify import markdownify as md, MarkdownConverter
from bs4 import BeautifulSoup

from src.utils.constants import BASE_URL_WIKI


class WikiMarkdownConverter(MarkdownConverter):
    """Custom converter for MediaWiki HTML."""

    def convert_a(self, el, text, convert_as_inline):
        """Convert links, normalizing wiki URLs."""
        href = el.get("href", "")

        # Skip empty or anchor-only links
        if not href or href.startswith("#"):
            return text

        # Normalize relative wiki links
        if href.startswith("/en-us/"):
            href = BASE_URL_WIKI + href.replace("/en-us", "")
        elif href.startswith("/wiki/"):
            href = BASE_URL_WIKI + href

        # Skip image links
        if "/images/" in href or el.find("img"):
            return text

        return f"[{text}]({href})"


def html_to_markdown(html: str) -> str:
    """
    Convert HTML string to clean markdown.

    Args:
        html: Raw HTML content from wiki page

    Returns:
        Clean markdown string
    """
    if not html or not html.strip():
        return ""

    # Pre-process: remove unwanted elements
    soup = BeautifulSoup(html, "html.parser")

    # Remove edit section links
    for element in soup.select(".mw-editsection"):
        element.decompose()

    # Remove script/style tags
    for tag in soup.find_all(["script", "style"]):
        tag.decompose()

    # Convert to markdown
    markdown = md(
        str(soup),
        heading_style="ATX",
        bullets="-",
        strip=["span"],
    )

    # Post-process cleanup
    markdown = clean_markdown(markdown)

    return markdown


def clean_markdown(text: str) -> str:
    """
    Clean up markdown artifacts.

    Args:
        text: Raw markdown text

    Returns:
        Cleaned markdown text
    """
    if not text:
        return ""

    # Remove [edit] markers
    text = re.sub(r'\[edit\]', '', text, flags=re.IGNORECASE)

    # Remove excessive blank lines (more than 2)
    text = re.sub(r'\n{3,}', '\n\n', text)

    # Remove leading/trailing whitespace from lines
    lines = [line.strip() for line in text.split('\n')]
    text = '\n'.join(lines)

    # Remove empty list items
    text = re.sub(r'^-\s*$', '', text, flags=re.MULTILINE)

    # Normalize link whitespace
    text = re.sub(r'\[\s+', '[', text)
    text = re.sub(r'\s+\]', ']', text)

    # Remove empty paragraphs
    text = re.sub(r'\n\n+', '\n\n', text)

    return text.strip()


def extract_ability_names(html: str) -> list[str]:
    """
    Extract ability names from abilities HTML section.

    Args:
        html: HTML containing ability definitions

    Returns:
        List of ability name strings
    """
    if not html:
        return []

    soup = BeautifulSoup(html, "html.parser")
    abilities = []

    # Try dl/dt pattern (definition list)
    for dt in soup.find_all("dt"):
        strong = dt.find("strong")
        if strong:
            abilities.append(strong.get_text(strip=True))
        else:
            text = dt.get_text(strip=True)
            if text:
                abilities.append(text)

    # Fallback: look for bold text
    if not abilities:
        for strong in soup.find_all(["strong", "b"]):
            text = strong.get_text(strip=True)
            if text and len(text) < 50:  # Ability names are short
                abilities.append(text)

    return abilities


def convert_list_to_markdown(html: str) -> str:
    """
    Convert HTML list to markdown bullet list.

    Args:
        html: HTML containing ul/ol elements

    Returns:
        Markdown bullet list
    """
    if not html:
        return ""

    soup = BeautifulSoup(html, "html.parser")
    items = []

    for li in soup.find_all("li"):
        text = li.get_text(strip=True)
        if text:
            items.append(f"- {text}")

    return "\n".join(items)
```

### Step 2: Create MarkdownConversionPipeline

Add to `src/scraper/pipelines.py`:

```python
from src.scraper.markdown_converter import html_to_markdown, extract_ability_names


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
        "trivia",
        "family",
        "occupations",
        "weapons",
        "regions",
        "factions",
    ]

    def process_item(self, item: dict, spider) -> dict:
        """Convert HTML fields to markdown."""

        # Convert content sections
        for field in self.HTML_FIELDS:
            if field in item and item[field]:
                original = item[field]
                item[field] = html_to_markdown(original)
                if item[field] != original:
                    spider.logger.debug(f"Converted {field} to markdown")

        # Special handling for abilities - extract names AND convert content
        if "abilities" in item and item["abilities"]:
            if isinstance(item["abilities"], str):
                # Extract ability names as list
                ability_names = extract_ability_names(item["abilities"])
                # Also keep markdown version for reference
                item["abilities_markdown"] = html_to_markdown(item["abilities"])
                item["abilities"] = ability_names

        return item
```

### Step 3: Update settings.py

```python
ITEM_PIPELINES = {
    "src.scraper.pipelines.MarkdownConversionPipeline": 200,
    "src.scraper.pipelines.PydanticValidationPipeline": 300,
}
```

### Step 4: Update PydanticValidationPipeline

Handle the new `abilities` structure:

```python
def _parse_abilities(self, abilities_data: Any) -> list[str]:
    """Parse abilities into list of strings."""
    if isinstance(abilities_data, list):
        return [str(a) for a in abilities_data if a]
    if isinstance(abilities_data, str):
        # Split by newlines if markdown, otherwise return as single item
        if "\n" in abilities_data:
            return [line.strip() for line in abilities_data.split("\n") if line.strip()]
        return [abilities_data] if abilities_data else []
    return []
```

---

## Todo List

- [ ] Add `markdownify>=0.14.0` to pyproject.toml (if not done)
- [ ] Create `src/scraper/markdown_converter.py`
- [ ] Implement `html_to_markdown()` function
- [ ] Implement `clean_markdown()` helper
- [ ] Implement `extract_ability_names()` helper
- [ ] Implement `WikiMarkdownConverter` class for custom link handling
- [ ] Add `MarkdownConversionPipeline` to pipelines.py
- [ ] Update pipeline priority in settings.py
- [ ] Test conversion with sample HTML
- [ ] Verify links normalized correctly
- [ ] Verify lists converted properly

---

## Success Criteria

- [ ] Background section converted to clean markdown paragraphs
- [ ] Wiki links converted to `[text](url)` format
- [ ] Lists converted to markdown bullet lists (`-`)
- [ ] No HTML tags in final output
- [ ] Edit markers removed
- [ ] Abilities extracted as name list

---

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Complex nested HTML | Medium | Medium | Use BeautifulSoup preprocessing |
| Broken links | Medium | Low | Normalize with BASE_URL_WIKI |
| Lost formatting | Low | Medium | Test with multiple champion pages |
| markdownify edge cases | Low | Low | Add post-processing cleanup |

---

## Security Considerations

- BeautifulSoup sanitizes HTML input
- No script/style tags in output
- URL normalization prevents injection

---

## Next Steps

After completing this phase:
1. Proceed to [Phase 05: Testing & Validation](./phase-05-testing-validation.md)
2. Run full crawl with 3 champions
3. Validate JSON output quality
