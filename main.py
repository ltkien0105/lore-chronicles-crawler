from bs4 import BeautifulSoup
import json

# from playwright.sync_api import sync_playwright
from lib.utils import get_all_links, get_n_next_siblings


def main():
    # url = "https://leagueoflegends.fandom.com/wiki/Timeline"
    # user_agent_list = [
    #     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 Edg/144.0.0.0",
    #     "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.94 Chrome/37.0.2062.94 Safari/537.36",
    #     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    #     "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    #     "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
    #     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/8.0.8 Safari/600.8.9",
    # ]

    # with sync_playwright() as p:
    #     browser = p.chromium.launch(
    #         headless=False,
    #         executable_path="E:\\Applications\\ms-playwright\\chromium-1194\\chrome-win\\chrome.exe",
    #     )
    #     page = browser.new_page(user_agent=random.choice(user_agent_list))
    #     page.goto(url, wait_until="domcontentloaded")
    #     content = page.content()
    #     browser.close()
    # write_content("timeline.json", content)

    with open("output.html", "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
        links = get_all_links(soup)
        with open("resources/timeline.json", "w", encoding="utf-8") as out_file:
            json.dump(
                {
                    "endpoint": "https://leagueoflegends.fandom.com/wiki/Timeline",
                    "links": links,
                },
                out_file,
                ensure_ascii=False,
                indent=4,
            )


if __name__ == "__main__":
    main()
