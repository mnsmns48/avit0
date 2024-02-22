import time
from selenium.common import TimeoutException
from seleniumbase import SB
from seleniumbase.common.exceptions import NoSuchElementException
from sqlalchemy.orm import Session

from DB.crud import sync_write_data
from DB.engine import sync_db
from func import get_info


def start_pars(link: str, start_page: int, pages: int, output_print: bool, db_rec: bool, sleep_time: int):
    if start_page != 1:
        url = f'{link}?p={start_page}'
    else:
        url = link
    count = start_page
    with SB(uc=True, browser='chrome', headed=False, page_load_strategy='eager', block_images=True) as driver:
        driver.get(url)
        while count != pages:
            try:
                elems = list()
                items = driver.find_elements("[data-marker='item']", by="css selector")
                for line in items:
                    page = line.get_attribute('innerHTML')
                    item = get_info(page)
                    elems.append(item)
                if output_print:
                    for i in elems:
                        for k, v in i.items():
                            print(f"{k}: {v}")
                        print('\n')
                    print('\n-------------------\n')
                if db_rec:
                    with Session(bind=sync_db.engine) as session:
                        sync_write_data(session=session, data=elems)
                    print(f'page: {count} added: {count * 50} lines')
                time.sleep(sleep_time)
                driver.find_element("[data-marker='pagination-button/nextPage']", by="css selector").click()
                count += 1
            except (TimeoutException, NoSuchElementException) as time_error:
                time.sleep(30)
                print(f"page: {count}\n{time_error}")
            except AttributeError as attribute_error:
                print(f"page: {count}\n{attribute_error}")
                count += 1
                new_link = f'{link}?p={count}'
                driver.get(new_link)
