import asyncio

from sqlalchemy.orm import Session

from DB.engine import sync_db
from DB.models import Base
from t_cls import Avito



def main():
    # Base.metadata.create_all(sync_db.engine)
    # start = Avito(url="https://bot.sannysoft.com",
    #               count=5,
    #               items=['']
    #               )
    # # start.parse()
    test_func()


# https://bot.sannysoft.com/

if __name__ == '__main__':
    try:
        main()

    except (KeyboardInterrupt, SystemExit):
        print('Script stopped')
