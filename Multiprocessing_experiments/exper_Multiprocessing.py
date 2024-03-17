import threading
import time
import multiprocessing

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from seleniumbase import Driver

from config import russia_eng

threadLocal = threading.local()


class DriverBrowser:
    def __init__(self):
        self.driver = Driver(uc=True, browser='chrome', headed=True, page_load_strategy='eager', block_images=True)

    def __del__(self):
        self.driver.quit()

    @classmethod
    def start_driver(cls):
        driver = getattr(threadLocal, 'driver', None)
        if driver is None:
            driver = cls()
            threadLocal.driver = driver
        return driver.driver


def region_check(region_id: int) -> None:
    time.sleep(1)
    result = dict()
    links_list = list()
    driver = DriverBrowser.start_driver()
    url = f"https://avito.ru/{russia_eng[region_id]}/gotoviy_biznes"
    driver.get(url)
    try:
        result['region'] = driver.find_element(By.XPATH, "//*[@class='desktop-nev1ty']").text
        submenu = driver.find_element(By.CSS_SELECTOR, "[class*='rubricator-list-item-submenu']")
        categories = submenu.text.split('\n')
        for item_menu in categories:
            obj = driver.find_element(By.CSS_SELECTOR, f'[title="{item_menu}"]')
            links_list.append(obj.get_attribute('href'))
        result['links'] = {k: v for k, v in zip(categories, links_list)}
        print(result)
    except NoSuchElementException:
        time.sleep(30)
        driver.get(url)


def main():
    items = list(range(0, len(russia_eng)))
    start = time.time()
    with multiprocessing.Pool(processes=2) as pool:
        ar = pool.map_async(region_check, items)
        ar.get()
    print('Done:', time.time() - start)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('script stopped')
