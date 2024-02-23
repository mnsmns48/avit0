import random
import re
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


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
                return datetime.now() - timedelta(**params) - timedelta(hours=random.randint(0, 12)) - timedelta(
                    minutes=random.randint(0, 59))
            else:
                return datetime.now() - timedelta(**params)


def get_seller(soup: BeautifulSoup) -> dict:
    seller_result = dict()
    seller_result['seller'] = None
    seller_result['seller_rank'] = None
    seller_result['seller_info'] = None
    seller = soup.find("div", {"class": re.compile('.*iva-item-userInfoStep-.*')})
    if not seller:
        return seller_result
    else:
        seller_info = seller.getText()
        if ',' in seller_info:
            seller_rank = re.search(r'[\d][,][\d]', seller_info).group()
            seller_result['seller'] = seller_info.split(seller_rank)[0]
            seller_reviews = seller_info.split(seller_rank)[1]
            seller_result['seller_rank'] = float(seller_rank.replace(',', '.'))
        else:
            seller_pattern = re.search(r"[Н|\d][е|\d|\s]", seller_info).group()
            seller_result['seller'] = seller_info.split(seller_pattern)[0]
            seller_reviews = seller_pattern + seller_info.split(seller_pattern)[1]
    seller_reviews_result = seller_reviews[0]
    for symbol in seller_reviews[1:]:
        if symbol.isupper():
            seller_reviews_result += f' {symbol}'
        else:
            seller_reviews_result += symbol
    seller_result['seller_info'] = seller_reviews_result
    return seller_result


def get_info(elem: str) -> dict:
    result = dict()
    soup = BeautifulSoup(elem, 'lxml')
    date = soup.find("div", {"class": re.compile('.*iva-item-dateInfoStep-.*')})
    loc = soup.find("div", {"class": re.compile('.*geo-root-.*')})
    price = soup.find(itemprop='price').get('content')
    title = soup.find(itemprop='name').getText()
    desc = soup.find("div", {"class": re.compile('.*iva-item-descriptionStep-.*')})
    link = soup.find(itemprop='url').get('href')
    result['date'] = date_convert(date.getText())
    result['location_1'] = link.split('/')[1]
    result['location_2'] = loc.getText()
    result['price'] = int(price)
    result['title'] = title
    result['description'] = desc.getText()
    result['link'] = 'https://www.avito.ru' + link
    seller = get_seller(soup)
    result.update(seller)
    return result
