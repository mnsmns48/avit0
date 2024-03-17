import os
import random
import time
from pathlib import Path

import undetected_chromedriver as uc
from selenium.common import StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from seleniumbase.common.exceptions import NoSuchElementException
from sqlalchemy.orm import Session

from DB.crud import add_support_info
from DB.engine import sync_db
from config import russia_rus

path = Path(os.path.abspath(__file__)).parent


def run_up_driver() -> uc:
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
    driver.implicitly_wait(10)
    driver.get('https://www.google.ru')
    time.sleep(random.uniform(0.4, 1))
    driver.find_element(By.XPATH, '//textarea[@aria-label]').send_keys('Avito')
    time.sleep(random.uniform(0.4, 1))
    driver.find_element(By.XPATH, '//input[@aria-label]').click()
    time.sleep(random.uniform(0.4, 1))
    driver.find_element(By.XPATH, '//h3[1]').click()
    time.sleep(random.randint(1, 3))
    driver.switch_to.window(driver.window_handles[1])
    driver.find_element(By.XPATH, "//button[@data-marker='top-rubricator/all-categories']").click()
    time.sleep(random.uniform(0.4, 0.8))
    menu = driver.find_elements(By.XPATH, "//div[contains(@class, 'new-rubricator-content-rootCategory-')]/div/p")
    for item in menu:
        ActionChains(driver).move_to_element(item).perform()
        time.sleep(random.uniform(0.1, 0.2))
    driver.find_element(By.XPATH, '//strong[@data-name="Готовый бизнес"]').click()
    time.sleep(random.uniform(0.4, 0.8))
    return driver


def region_check_v3(region: str, driver: uc) -> dict:
    ignored_exceptions = (NoSuchElementException, StaleElementReferenceException)
    WebDriverWait(driver=driver,
                  timeout=3,
                  ignored_exceptions=ignored_exceptions) \
        .until(expected_conditions.presence_of_element_located((By.XPATH, '//span[@class="desktop-nev1ty"]'))).click()
    time.sleep(random.uniform(0.4, 1))
    WebDriverWait(driver=driver,
                  timeout=3,
                  ignored_exceptions=ignored_exceptions) \
        .until(expected_conditions.presence_of_element_located((By.XPATH, '//div[@data-marker="clear-icon"]'))).click()
    time.sleep(random.uniform(0.4, 1))
    WebDriverWait(driver=driver,
                  timeout=3,
                  ignored_exceptions=ignored_exceptions) \
        .until(expected_conditions.presence_of_element_located(
        (By.XPATH, '//input[@placeholder="Город или регион"]'))).send_keys(region)
    time.sleep(random.uniform(1, 2))
    cities = driver.find_elements(By.XPATH, "//span[contains(@class, 'suggest-suggest_content-')]")
    time.sleep(random.uniform(0.4, 0.6))

    for i in cities:
        if i.text == russia_rus.get(region):
            WebDriverWait(driver=i,
                          timeout=3,
                          ignored_exceptions=ignored_exceptions) \
                .until(expected_conditions.presence_of_element_located((By.XPATH, '../..'))).click()
            break
    time.sleep(2)
    WebDriverWait(driver=driver,
                  timeout=2,
                  ignored_exceptions=ignored_exceptions) \
        .until(expected_conditions
               .presence_of_element_located((By.XPATH, '//button[@data-marker="popup-location/save-button"]'))).click()
    result = dict()
    result['region'] = WebDriverWait(driver=driver,
                                     timeout=3,
                                     ignored_exceptions=ignored_exceptions) \
        .until(expected_conditions
               .presence_of_element_located((By.XPATH, '//span[@class="desktop-nev1ty"]'))).text
    submenu = driver.find_elements(By.XPATH, "//div[contains(@class, 'rubricator-list-item-')]/a")[1:]
    categories_nms = [i.text for i in submenu]
    links = [i.get_attribute('href') for i in submenu]
    result['links'] = {k: v for k, v in zip(categories_nms, links)}
    print(f'{result.get("region")} добавлен')
    return result


def save_links_v3():
    driver = run_up_driver()
    for region in russia_rus.keys():
        data = region_check_v3(driver=driver, region=region)
        with Session(bind=sync_db.engine) as session:
            add_support_info(session=session, data=data)
