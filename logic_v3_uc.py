import os
import random
import time
from pathlib import Path

import undetected_chromedriver as uc
from selenium.common import StaleElementReferenceException, TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from seleniumbase.common.exceptions import NoSuchElementException, WebDriverException
from sqlalchemy.orm import Session

from DB.crud import add_support_info
from DB.engine import sync_db
from config import russia_eng, hidden, russia_rus

path = Path(os.path.abspath(__file__)).parent


def get_region_links_v3():
    items = list(range(0, len(russia_eng)))
    start = time.time()
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument('--blink-settings=imagesEnabled=false')
    chrome_options.add_experimental_option(
        "prefs", {"profile.managed_default_content_settings.images": 2}
    )
    driver = uc.Chrome(headless=False,
                       use_subprocess=False,
                       version_main=114,
                       driver_executable_path=f'{path}/chromedriver',
                       chrome_options=chrome_options)
    driver.maximize_window()
    driver.implicitly_wait(3)
    driver.get('https://www.google.ru')
    time.sleep(random.uniform(0.4, 1))
    driver.find_element(By.XPATH, '//textarea[@aria-label]').send_keys('Avito')
    time.sleep(random.uniform(0.4, 1))
    driver.find_element(By.XPATH, '//input[@aria-label]').click()
    time.sleep(random.uniform(0.4, 1))
    driver.find_element(By.XPATH, '//h3[1]').click()
    time.sleep(random.randint(1, 3))
    driver.switch_to.window(driver.window_handles[1])
    for line in items:
        while True:
            try:
                data = region_check_v3(region_id=line,
                                       driver=driver)
                break
            except (WebDriverException, StaleElementReferenceException):
                time.sleep(3)
                driver.refresh()
                continue
        with Session(bind=sync_db.engine) as session:
            add_support_info(session=session, data=data)
    print(f'\nЗадержка {hidden.delay}\nВремя выполнения: {time.time() - start} секунд\n'
          f'Области добавлены')


def region_check_v3(region_id: id, driver: uc) -> dict:
    driver.find_element(By.XPATH, '//span[@class="desktop-nev1ty"]').click()
    time.sleep(random.uniform(0.4, 1))
    driver.find_element(By.XPATH, '//div[@data-marker="clear-icon"]').click()
    time.sleep(random.uniform(0.4, 1))
    driver.find_element(By.XPATH, '//input[@placeholder="Город или регион"]').send_keys(russia_rus[region_id])
    time.sleep(random.uniform(0.4, 1))
    cities = driver.find_elements(By.XPATH, "//span[contains(@class, 'suggest-suggest_content-')]")
    time.sleep(random.uniform(0.4, 0.6))
    ignored_exceptions = (NoSuchElementException, StaleElementReferenceException)
    for i in cities:
        if i.text == russia_rus[region_id]:
            accept = WebDriverWait(driver=i,
                                   timeout=2,
                                   ignored_exceptions=ignored_exceptions) \
                .until(expected_conditions.presence_of_element_located((By.XPATH, '../..')))
            if accept:
                accept.click()
            break
    time.sleep(2)
    search_button = WebDriverWait(driver=driver,
                                  timeout=2,
                                  ignored_exceptions=ignored_exceptions) \
        .until(expected_conditions
               .presence_of_element_located((By.XPATH, '//button[@data-marker="popup-location/save-button"]')))
    if search_button:
        search_button.click()
    time.sleep(60)
