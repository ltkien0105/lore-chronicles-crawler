"""
HTML to Markdown conversion utilities.
"""
import re
from markdownify import markdownify as md
from bs4 import BeautifulSoup

from src.utils.constants import BASE_URL_WIKI


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

    # Remove image-only spans (inline icons)
    for span in soup.select("span.inline-image"):
        # Keep the text but remove the span wrapper with images
        img = span.find("img")
        if img:
            img.decompose()

    # Normalize links before conversion
    for a in soup.find_all("a"):
        href = a.get("href", "")
        if href:
            # Normalize relative wiki links
            if href.startswith("/en-us/"):
                a["href"] = BASE_URL_WIKI + href.replace("/en-us", "")
            elif href.startswith("/wiki/"):
                a["href"] = BASE_URL_WIKI + href

    # Convert to markdown
    markdown = md(
        str(soup),
        heading_style="ATX",
        bullets="-",
        strip=["span", "img"],
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
    text = re.sub(r'\[edit source\]', '', text, flags=re.IGNORECASE)

    # Remove excessive blank lines (more than 2)
    text = re.sub(r'\n{3,}', '\n\n', text)

    # Remove leading/trailing whitespace from lines
    lines = [line.rstrip() for line in text.split('\n')]
    text = '\n'.join(lines)

    # Remove empty list items
    text = re.sub(r'^-\s*$', '', text, flags=re.MULTILINE)

    # Normalize link whitespace
    text = re.sub(r'\[\s+', '[', text)
    text = re.sub(r'\s+\]', ']', text)

    # Clean up empty markdown links []()
    text = re.sub(r'\[\]\([^)]*\)', '', text)

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

    # Try li > b pattern (list items with bold ability names)
    for li in soup.find_all("li"):
        # Look for bold text at start of list item
        b = li.find(["b", "strong"])
        if b:
            text = b.get_text(strip=True)
            # Clean up ability name - remove colons and trailing text
            if ":" in text:
                text = text.split(":")[0].strip()
            if text and len(text) < 100:
                abilities.append(text)

    # Fallback: Try dl/dt pattern (definition list)
    if not abilities:
        for dt in soup.find_all("dt"):
            strong = dt.find("strong")
            if strong:
                abilities.append(strong.get_text(strip=True))
            else:
                text = dt.get_text(strip=True)
                if text:
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
