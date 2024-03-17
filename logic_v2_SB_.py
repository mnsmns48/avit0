import random
import threading
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from seleniumbase import SB
from seleniumbase.common.exceptions import NoSuchElementException, ElementNotVisibleException, TimeoutException
from sqlalchemy.orm import Session

from DB.crud import add_support_info, get_links, sync_write_data
from DB.engine import sync_db
from config import russia_eng, hidden, category_dict
from bs4_process import pars_one_ad, time_count


# threadLocal = threading.local()


def region_check(region_id: int, driver: SB) -> dict:
    time.sleep(hidden.delay)
    result = dict()
    links_list = list()
    url = f"https://avito.ru/{russia_eng[region_id]}/gotoviy_biznes"
    driver.get(url)
    while True:
        try:
            result['region'] = driver.find_element(By.XPATH, '//span[@class="desktop-nev1ty"]').text
            print(result['region'])
        except NoSuchElementException:
            print(f'Ошибка парсинга области {russia_eng[region_id]}\n'
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


def get_region_links_v2():
    items = list(range(0, len(russia_eng)))
    start = time.time()
    with SB(uc=True, browser='chrome', headed=False, page_load_strategy='eager', block_images=True) as driver:
        for line in items:
            data = region_check(region_id=line,
                                driver=driver)
            with Session(bind=sync_db.engine) as session:
                add_support_info(session=session, data=data)
        print(f'\nЗадержка {hidden.delay}\nВремя выполнения: {time.time() - start} секунд\n'
              f'Области добавлены')


@time_count
def pars_region(reg_n: int):
    with SB(uc=True, browser='chrome', headed=False, page_load_strategy='eager', block_images=True) as driver:
        links = get_links(region_id=reg_n)
        region = links.get('region')
        links.pop('region')
        # links.pop('franshizy')
        # links.pop('proizvodstvo')
        # links.pop('internet_magazin')
        # links.pop('sfera_uslug')
        # links.pop('selskoe_hozyaystvo')
        # links.pop('avtomobilnyi_biznes')
        # links.pop('zdorove_i_medicina')
        # links.pop('obschestvennoe_pitanie')
        # links.pop('drugoe')
        # links.pop('razvlecheniya')
        # links.pop('stroitelstvo')
        # links.pop('torgovlya')
        # links.pop('krasota_i_ukhod')
        # links.pop('gostinicy_i_bazy_otdykha')
        keys = list(links.keys())
        for link_key in keys:
            category = category_dict.get(link_key)
            link = links.get(link_key)
            print(f'{region} {category}')
            if link:
                start_page_number = int(link.rsplit('=')[1])
                driver.get(link)
                while True:
                    try:
                        ads_list_text = driver.find_element('[data-marker="catalog-serp"]', by='css selector')
                    except ElementNotVisibleException:
                        break
                    except (NoSuchElementException, TimeoutException):
                        print('NoSuchElementException Handled - 1')
                        time.sleep(35)
                        driver.refresh()
                        ads_list_text = driver.find_element('[data-marker="catalog-serp"]', by='css selector')
                    ads_soup = BeautifulSoup(markup=ads_list_text.get_attribute('innerHTML'),
                                             features='lxml')
                    ads_list = ads_soup.find_all('div', attrs={'data-marker': 'item'})
                    elems = list()
                    for ad in ads_list:
                        elem = pars_one_ad(elem=str(ad), region=region, category=category)
                        elems.append(elem)
                    with Session(bind=sync_db.engine) as session:
                        sync_write_data(session=session, data=elems)
                    print(f'page: {start_page_number} added: {start_page_number * 50} lines')
                    time.sleep(random.randint(1, 5))
                    try:
                        click = driver.find_element("[data-marker='pagination-button/nextPage']",
                                                    by="css selector").get_attribute('href')
                        if click:
                            driver.find_element("[data-marker='pagination-button/nextPage']",
                                                by="css selector").click()
                            start_page_number += 1
                        else:
                            break
                    except NoSuchElementException:
                        print('NoSuchElementException Handled - 2')
                        break
                    except TimeoutException:
                        time.sleep(31)
                        driver.refresh()
