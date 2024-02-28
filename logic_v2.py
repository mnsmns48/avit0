import time

from selenium.webdriver.common.by import By
from seleniumbase import Driver
from seleniumbase.common.exceptions import NoSuchElementException

from DB.crud import add_support_info
from config import russia


def region_check(region_id: int, driver: Driver) -> dict:
    time.sleep(0.9)
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
            print(f'{result.get("region")} добавлен')
            return result
        except NoSuchElementException:
            print(f'Ошибка парсинга области {russia[region_id]}\n'
                  'Пробую через 30 секунд опять')
            time.sleep(30)
            driver.get(url)


def logic_v2():
    items = [28, 27]
    # items = list(range(0, len(russia)))
    start = time.time()
    driver = Driver(uc=True, browser='chrome', headed=True, page_load_strategy='eager', block_images=True)
    for line in reversed(items):
        data = region_check(region_id=line,
                            driver=driver)
        add_support_info(data)
    driver.close()
    print('Время выполнения:', time.time() - start, 'секунд')
