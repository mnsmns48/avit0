# url = 'https://whoer.net'
# proxy = "185.238.228.48:80"
#
# if __name__ == "__main__":
#     with SB(uc=True,
#             browser='chrome',
#             headed=True,
#             page_load_strategy='eager',
#             block_images=True,
#             proxy=proxy) as driver:
#         driver.get(url)
#         time.sleep(60)
#
#
# file = open('file2.html', 'r')
# lines = file.readlines()
# file.close()
# html = ''.join(lines)
#
import time
import random

import multiprocessing
from selenium.webdriver.common.by import By
from seleniumbase import SB, Driver
from seleniumbase.undetected import WebElement

from config import russia, internal_links
from func import date_convert


# def get_info(elem: WebElement) -> dict:
#     title = elem.find_element(By.CSS_SELECTOR, '[itemprop="name"]').text
#     date = elem.find_element(By.CSS_SELECTOR, '[data-marker="item-date"]').text
#     # date_test = WebDriverWait(elem, 2).until(EC.visibility_of_element_located((By.XPATH, "//*[@data-marker='item-date']")))
#     price = elem.find_element(By.CSS_SELECTOR, "[itemprop='price']").get_attribute('content')
#     description = elem.find_element(By.CSS_SELECTOR, "[class*='iva-item-description']").text
#     link = elem.find_element(By.CSS_SELECTOR, '[itemprop="url"]').get_attribute('href')
#     # loc = elem.find_element(By.CSS_SELECTOR, "[style='-webkit-line-clamp:1']").text
#     result = {
#         'id': None,
#         'date': date_convert(date),
#         'loc': link.split('https://www.avito.ru/')[1].split('/')[0],
#         'price': price,
#         'seller': None,
#         'seller_rank': None,
#         'seller_reviews': None,
#         'title': title,
#         'description': description,
#         'link': link,
# 'm_seller': check_seller.text if check_seller else None
# 'm_seller': [i.text for i in m_seller],
# }
# return result


# if __name__ == "__main__":
#     with SB(uc=True,
#             browser='chrome',
#             headed=True,
#             page_load_strategy='eager',
#             block_images=True) as driver:
#         category = [cat for cat in internal_links]
#         for i in category:
#             url = russia[0] + internal_links.get(i)
#             driver.get(url)
#             time.sleep(10)


# def open_page(url: str):
#     with SB(uc=True,
#             browser='chrome',
#             headed=True,
#             page_load_strategy='eager',
#             block_images=True) as page:
#         page.get(url)
def region_check(driver: Driver, region_id: int) -> dict:
    result = dict()
    links_list = list()
    url = f"https://avito.ru/{russia[region_id]}/gotoviy_biznes"
    driver.get(url)
    result['region'] = driver.find_element(By.XPATH, "//*[@class='desktop-nev1ty']").text
    submenu = driver.find_element(By.CSS_SELECTOR, "[class*='rubricator-list-item-submenu']")
    categories = submenu.text.split('\n')
    for item_menu in categories:
        obj = driver.find_element(By.CSS_SELECTOR, f'[title="{item_menu}"]')
        links_list.append(obj.get_attribute('href'))
    result['links'] = {k: v for k, v in zip(categories, links_list)}
    print(result)



if __name__ == "__main__":
    start = time.time()
    items = list(range(0, len(russia)))
    p = multiprocessing.Pool(processes=3)
    p.map()


    with multiprocessing.Pool(processes=3) as pool:
        main_driver = Driver(uc=True, browser='chrome', headed=True, page_load_strategy='eager', block_images=True)
        pool.map(region_check, items)
        main_driver.close()
            # region = region_check(driver=main_driver, region_id=item)
    print(time.time() - start)

    # with multiprocessing.Pool(processes=1) as pool:
    #     result = pool.map_async(driver_start, url_1)
    #     result.get()
