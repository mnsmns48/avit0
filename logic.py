import random
import time

from seleniumbase import SB
from sqlalchemy.orm import Session

from DB.crud import sync_write_data
from DB.engine import sync_db
from func import get_info


def start_pars(url: str, pages: int):
    count = 1
    with SB(uc=True, browser='chrome', headed=True, page_load_strategy='eager', block_images=True) as driver:
        driver.get(url)
        while count != pages + 1:
            items = driver.find_elements("[data-marker='item']", by="css selector")
            result: list = list(map(get_info, items))
            #         print('------------')
            with Session(bind=sync_db.engine) as session:
                sync_write_data(session=session, data=result)
            # session.close()
            # time.sleep(random.randint(8, 15))
            driver.find_element("[data-marker='pagination-button/nextPage']", by="css selector").click()
            count += 1
            time.sleep(random.randint(2, 5))
