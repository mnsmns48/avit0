from sqlalchemy.exc import OperationalError

from DB.crud import out_excel, create_db, get_regions_db, write_region_data
from DB.engine import sync_db
from DB.models import Base
from logic import get_region_links, pars_region


def main():
    try:
        Base.metadata.create_all(sync_db.engine)
    except OperationalError:
        create_db()
        Base.metadata.create_all(sync_db.engine)
    print('Что парсим?\n'
          '1 - Спарсить ссылки по всем регионам\n'
          '2 - Парсим область\n'
          '3 - Парсим всю Россию\n'
          '8 - Забираем результаты')
    choice = int(input())
    if choice == 1:
        print('Забираю ссылки')
        get_region_links()
        print('Начинаю собирать по областям')
    if choice == 2:
        print('Введите номер региона')
        n = int(input())
        pars_region(reg_n=n)
    if choice == 3:
        print('Выбран режим парсинга всей России')
        regions = list(range(0, 84))
        # regions = [68, 69]
        for region_id in regions:
            pars_region(reg_n=region_id)
    if choice == 8:
        print('Создаю Excel файл с данными')
        regions = get_regions_db()
        for reg in regions:
            write_region_data(reg)


if __name__ == '__main__':
    main()
