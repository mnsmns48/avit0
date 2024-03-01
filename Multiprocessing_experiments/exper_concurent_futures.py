import time
import random

import concurrent.futures
from itertools import cycle

from selenium.webdriver.common.by import By
from seleniumbase import Driver

from config import russia


def region_check(driver: Driver, region_id: int) -> dict:
    time.sleep(1)
    items = list(range(0, len(russia)))
    random.shuffle(items)
    result = dict()
    links_list = list()
    url = f"https://avito.ru/{russia[region_id]}/gotoviy_biznes"
    driver.get(url)
    while True:
        try:
            result['region'] = driver.find_element(By.XPATH, "//*[@class='desktop-nev1ty']").text
            submenu = driver.find_element(By.CSS_SELECTOR, "[class*='rubricator-list-item-submenu']")
            categories = submenu.text.split('\n')
            for item_menu in categories:
                obj = driver.find_element(By.CSS_SELECTOR, f'[title="{item_menu}"]')
                links_list.append(obj.get_attribute('href'))
            result['links'] = {k: v for k, v in zip(categories, links_list)}
            print(result)
            break
        except:
            time.sleep(30)
            driver.get(url)


def callback(result):
    print(result)


def main():
    start = time.time()
    items = list(range(0, len(russia)))
    drivers = [
        Driver(uc=True, browser='chrome', headed=True, page_load_strategy='eager', block_images=True),
        Driver(uc=True, browser='chrome', headed=True, page_load_strategy='eager', block_images=True),
    ]
    args = list()
    for i in zip(cycle(drivers), reversed(items)):
        args.append(i)
    with concurrent.futures.ProcessPoolExecutor(max_workers=2) as executor:
        r = executor.map(region_check, args)
        next(r)
    for driver in drivers:
        driver.close()
    print('Done:', time.time() - start)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('script stopped')
