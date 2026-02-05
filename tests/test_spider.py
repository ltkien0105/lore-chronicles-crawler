"""
Unit tests for LOL Wiki spider.
"""

import pytest
from scrapy.http import HtmlResponse, Request

from src.scraper.spiders.lol_wiki_spider import LolWikiSpider
from src.scraper.markdown_converter import (
    html_to_markdown,
    clean_markdown,
    extract_ability_names,
)


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
        assert clean_markdown("") == ""


class TestExtractAbilityNames:
    """Tests for ability name extraction."""

    def test_extract_from_list_bold(self):
        html = """
        <ul>
            <li><b>Rupture:</b> Creates a void explosion.</li>
            <li><b>Feral Scream:</b> Silences enemies.</li>
        </ul>
        """
        abilities = extract_ability_names(html)
        assert "Rupture" in abilities
        assert "Feral Scream" in abilities

    def test_extract_from_strong(self):
        html = """
        <ul>
            <li><strong>Master Axeman</strong></li>
            <li><strong>Extreme Resilience</strong></li>
        </ul>
        """
        abilities = extract_ability_names(html)
        assert "Master Axeman" in abilities
        assert "Extreme Resilience" in abilities

    def test_empty_input(self):
        assert extract_ability_names("") == []
        assert extract_ability_names(None) == []


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

    def test_extract_infobox_field_missing(self, mock_response):
        spider = LolWikiSpider()
        missing = spider._extract_infobox_field(mock_response, "NonExistent")
        assert missing == ""
