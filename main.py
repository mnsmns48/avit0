from config import russia
from sqlalchemy.exc import OperationalError

from DB.crud import out_excel, create_db
from DB.engine import sync_db
from DB.models import Base
from config import hidden
from logic import start_pars
from logic_v2 import logic_v2


def main():
    try:
        Base.metadata.create_all(sync_db.engine)
    except OperationalError:
        create_db()
        Base.metadata.create_all(sync_db.engine)
    print('Что парсим?\n'
          '1 - Спарсить ссылки по всем регионам\n'
          '8 - Забираем результаты')
    choice = int(input())
    if choice == 1:
        print('Забираю ссылки')
        logic_v2()
    if choice == 8:
        print('Создаю Excel файл с данными')
        out_excel()


if __name__ == '__main__':
    main()
    # start_pars(
    #     link=russia[0],
    #     start_page=hidden.start_page,
    #     pages=hidden.pages,
    #     output_print=False,
    #     db_rec=True,
    #     sleep_time=0
    # )
