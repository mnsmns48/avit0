import time

from seleniumbase import SB


def parse(url: str):
    with SB(uc=True,
            browser='chrome',
            headed=True,
            page_load_strategy='eager',
            block_images=True
            ) as driver:
        driver.get(url)
        time.sleep(20)
