"""Scrapy settings for lol_wiki_scraper project."""

BOT_NAME = "lol_wiki_scraper"

SPIDER_MODULES = ["src.scraper.spiders"]
NEWSPIDER_MODULE = "src.scraper.spiders"

# Crawl responsibly
ROBOTSTXT_OBEY = True
USER_AGENT = "LoreChroniclesCrawler/1.0 (+https://github.com/lore-chronicles-crawler)"

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

# Output settings - single champions.json file
FEED_EXPORT_ENCODING = "utf-8"
FEEDS = {
    "output/champions.json": {
        "format": "json",
        "encoding": "utf8",
        "indent": 2,
        "overwrite": True,
    }
}

# Pipelines
ITEM_PIPELINES = {
    "src.scraper.pipelines.MarkdownConversionPipeline": 200,
    "src.scraper.pipelines.PydanticValidationPipeline": 300,
}

# Logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s [%(name)s] %(levelname)s: %(message)s"
