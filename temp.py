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
from selenium.webdriver.common.by import By
from seleniumbase.undetected import WebElement

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
