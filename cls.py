import asyncio
import datetime

import undetected_chromedriver as uc
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from DB.crud import write_data
from DB.engine import db


class Avito:
    def __init__(self, url: str, items: list, count: int = 100):
        self.url = url
        self.items = items
        self.count = count

    async def __set_up(self):
        self.driver = uc.Chrome(headless=True, use_subprocess=True)

    async def __get_url(self):
        self.driver.get(self.url)

    async def __paginator(self):
        pag = self.driver.find_element(By.CSS_SELECTOR, '[data-marker="pagination-button/nextPage"]')
        while pag:
            await self.__parse_page()
            self.driver.find_element(By.CSS_SELECTOR, '[data-marker="pagination-button/nextPage"]').click()
            await asyncio.sleep(10)

    async def __parse_page(self):
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
                'seller': seller,
                'seller_rank': seller_rank

            })
            async with db.scoped_session() as session:
                await write_data(session=session, data=result)
            await asyncio.sleep(10)

    async def parse(self):
        await self.__set_up()
        await self.__get_url()
        await self.__paginator()
