 import asyncio
import datetime
import time
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from DB.crud import write_data
from DB.engine import sync_db
from DB.models import AvitoData

from selenium import webdriver


class Avito:
    def __init__(self, url: str, items: list, count: int = 100):
        self.url = url
        self.items = items
        self.count = count

    def __set_up(self):
        self.driver = uc.Chrome(headless=False, use_subprocess=True)

    def __get_url(self):
        self.driver.get(self.url)

    def __paginator(self):
        pag = self.driver.find_element(By.CSS_SELECTOR, '[data-marker="pagination-button/nextPage"]')
        while pag:
            self.__parse_page()
            self.driver.find_element(By.CSS_SELECTOR, '[data-marker="pagination-button/nextPage"]').click()
            time.sleep(10)

    def __parse_page(self):
        titles = self.driver.find_elements(By.CSS_SELECTOR, '[data-marker="item"]')
        for item in titles:
            result = dict()
            # elem = item.find_element(By.CSS_SELECTOR, '[class*="iva-item-dateInfoStep]')
            # date_ = ActionChains(self.driver).move_to_element(elem)
            name = item.find_element(By.CSS_SELECTOR, '[itemprop="name"]').text
            description = item.find_element(By.CSS_SELECTOR, "[class*='iva-item-description']").text
            link = item.find_element(By.CSS_SELECTOR, '[itemprop="url"]').get_attribute('href')
            price = item.find_element(By.CSS_SELECTOR, '[itemprop="price"]').get_attribute('content')
            # seller = 'None'
            # seller_rank = 5.2
            result.update({
                'date': datetime.datetime.now(),
                'price': int(price),
                'title': name,
                'description': description,
                'link': link,
                # 'seller': seller,
                # 'seller_rank': seller_rank

            })
            with Session(bind=sync_db.engine) as session:
                session.execute(insert(AvitoData).values(result))
                session.commit()
            time.sleep(5)

    def parse(self):
        self.__set_up()
        self.__get_url()
        time.sleep(60)