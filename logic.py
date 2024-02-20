import time
from bs4 import BeautifulSoup
import lxml
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from seleniumbase import SB
from sqlalchemy.orm import Session

from DB.crud import sync_write_data
from DB.engine import sync_db
from func import get_info, get_info


def start_pars(url: str, start_page: int, pages: int, output_print: bool, db_rec: bool, sleep_time: int):
    count = start_page
    with SB(uc=True, browser='chrome', headed=False, page_load_strategy='eager', block_images=True) as driver:
        driver.get(url)
        while count != pages + 1:
            try:
                elems = list()
                items = driver.find_elements("[data-marker='item']", by="css selector")
                print(count, 'page')
                for line in items:
                    item = get_info(line.get_attribute('innerHTML'))
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
                    print(f'added {count * 50} lines from start')
                time.sleep(sleep_time)
                driver.find_element("[data-marker='pagination-button/nextPage']", by="css selector").click()
                count += 1
            except TimeoutException as time_exception_error:
                print(f"page: {count}\n{time_exception_error}")
            except AttributeError as attribute_error:
                print(f"page: {count}\n{attribute_error}")
                driver.find_element("[data-marker='pagination-button/nextPage']", by="css selector").click()
