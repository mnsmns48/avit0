import time

from selenium.webdriver.common.by import By
from seleniumbase import SB


def parse(url: str):
    with SB(uc=True,
            browser='chrome',
            headed=True,
            page_load_strategy='eager',
            block_images=True,

            ) as driver:
        content = driver.get(url)
    titles = content.find_elements(By.CSS_SELECTOR, '[data-marker="item"]')
    for item in titles:
        name = item.find_element(By.CSS_SELECTOR, '[itemprop="name"]').text
        print(name)
    time.sleep(20)
