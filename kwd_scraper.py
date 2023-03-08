import re
from playwright.sync_api import  sync_playwright
from bs4 import BeautifulSoup

def Keyword_extractor_free(text):
    # text = """In 2023, farming and agriculture continue to be critical industries for food security and economic growth around the world."""

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://keywordextraction.net/keyword-extractor")
        page.fill('#text',text)
        page.locator('xpath=//input[@type="submit"]').click()
        html = page.inner_html('xpath=//div[@class="span5"]')
        soup = BeautifulSoup(html,'html.parser')
    # Find the <p> tag
    p_tag = soup.find('p')
    # Get all the text inside the <p> tag as a list
    kwds = [text.strip() for text in p_tag.stripped_strings]
    return kwds

