import random
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from seleniumbase.undetected import WebElement


def date_convert(date: str) -> datetime | None:
    units = {
        'час': 'hours',
        'мин': 'minutes',
        'дн': 'days',
        'день': 'days',
        'неде': 'weeks'
    }
    for key in units.keys():
        if key in date.split(' ')[1]:
            params = dict()
            params[units.get(key)] = int(date.split(' ')[0])
            if 'days' or 'weeks' in params.keys():
                return datetime.now() - timedelta(**params) - timedelta(hours=random.randint(0, 7)) - timedelta(
                    minutes=random.randint(0, 59))
            else:
                return datetime.now() - timedelta(**params)


def get_info(elem: WebElement) -> dict:
    title = elem.find_element(By.CSS_SELECTOR, '[itemprop="name"]').text
    date = elem.find_element(By.CSS_SELECTOR, '[data-marker="item-date"]').text
    # date_test = WebDriverWait(elem, 2).until(EC.visibility_of_element_located((By.XPATH, "//*[@data-marker='item-date']")))
    # m_seller = elem.find_elements(By.CSS_SELECTOR, '[style="-webkit-line-clamp:1"]')
    price = elem.find_element(By.CSS_SELECTOR, "[itemprop='price']").get_attribute('content')
    description = elem.find_element(By.CSS_SELECTOR, "[class*='iva-item-description']").text
    link = elem.find_element(By.CSS_SELECTOR, '[itemprop="url"]').get_attribute('href')
    # loc = elem.find_element(By.CSS_SELECTOR, "[style='-webkit-line-clamp:1']").text
    result = {
        'date': date_convert(date),
        'title': title,
        'price': price,
        'link': link,
        'description': description,
        'city': 'Санкт-Петербург',
        # 'm_seller': [i.text for i in m_seller],
        'seller': 'Продавец',
        'seller_rank': 0
    }
    return result


