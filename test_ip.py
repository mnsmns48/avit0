import time
from seleniumbase import SB

url = 'https://whoer.net'
proxy = "185.238.228.48:80"

if __name__ == "__main__":
    with SB(uc=True,
            browser='chrome',
            headed=True,
            page_load_strategy='eager',
            block_images=True,
            proxy=proxy) as driver:
        driver.get(url)
        time.sleep(60)
