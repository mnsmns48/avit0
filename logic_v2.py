import time

from selenium.webdriver.common.by import By
from seleniumbase import Driver
from seleniumbase.common.exceptions import NoSuchElementException
from sqlalchemy.orm import Session

from DB.crud import add_support_info, get_links
from DB.engine import sync_db
from config import russia
from config import hidden


def region_check(region_id: int, driver: Driver) -> dict:
    time.sleep(hidden.delay)
    result = dict()
    links_list = list()
    url = f"https://avito.ru/{russia[region_id]}/gotoviy_biznes"
    driver.get(url)
    while True:
        try:
            result['region'] = driver.find_element(By.XPATH, "//*[@class='desktop-nev1ty']").text
        except NoSuchElementException:
            print(f'Ошибка парсинга области {russia[region_id]}\n'
                  'Пробую через 30 секунд опять')
            time.sleep(30)
            driver.get(url)
        submenu = driver.find_element(By.CSS_SELECTOR, "[class*='rubricator-list-item-submenu']")
        categories = submenu.text.split('\n')
        for item_menu in categories:
            obj = driver.find_element(By.CSS_SELECTOR, f'[title="{item_menu}"]')
            links_list.append(obj.get_attribute('href'))
        result['links'] = {k: v for k, v in zip(categories, links_list)}
        print(f'{result.get("region")} добавлен')
        return result


def get_region_links():
    items = list(range(0, len(russia)))
    start = time.time()
    driver = Driver(uc=True, browser='chrome', headed=True, page_load_strategy='eager', block_images=True)
    for line in items:
        data = region_check(region_id=line,
                            driver=driver)
        with Session(bind=sync_db.engine) as session:
            add_support_info(session=session, data=data)
    driver.close()
    print(f'\nЗадержка {hidden.delay}\nВремя выполнения: {time.time() - start} секунд\n'
          f'Области добавлены')


def gen_region_info():
    print('Введите номер области')
    choice = int(input())
    with Session(bind=sync_db.engine) as session:
        links = get_links(session=session, region_id=choice)
    for k, v in links.items():
        print(k, v)